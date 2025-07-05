# Book Management System - PostgreSQL Database with Sharding

This directory contains the SQLAlchemy models for the Book Management System, implementing the ERD with PostgreSQL and branch-based sharding.

## 🗄️ Database Architecture

### PostgreSQL Setup
- **Primary Database**: Main database for non-sharded entities (authors, books, categories, users, branches)
- **Sharded Databases**: Separate databases for branch-specific data (physical exemplars, lending transactions)
- **Connection Pooling**: Optimized connection management with configurable pool sizes
- **Timezone Support**: All datetime fields use timezone-aware timestamps

### Sharding Strategy
- **Shard Key**: `branch_id` - All branch-specific data is sharded by branch
- **Sharded Tables**: `physical_exemplars`, `book_lending`
- **Non-Sharded Tables**: `authors`, `books`, `book_categories`, `users`, `user_types`, `branches`
- **Sharding Algorithm**: Hash-based distribution across available shards

## 📊 Models Overview

### Core Entities (Main Database)
1. **Author** - Book authors with indexed name field
2. **Book** - Books with ISBN uniqueness and comprehensive indexing
3. **BookData** - Book translations and additional metadata
4. **BookCategory** - Book categories/genres
5. **Branch** - Library branches (shard routing key)
6. **User** - Library users with type relationships
7. **UserType** - User types (Student, Teacher, etc.)

### Junction Tables (Main Database)
1. **AuthorBook** - Many-to-many relationship between authors and books
2. **CategoryBook** - Many-to-many relationship between categories and books

### Sharded Entities
1. **PhysicalExemplar** - Physical book copies (sharded by branch_id)
2. **BookLending** - Lending transactions (sharded by branch_id)

## 🔧 Configuration

### Environment Variables
```bash
# Main database
DATABASE_URL=postgresql://user:password@localhost:5432/book_service

# Sharded databases
DATABASE_URL_MAIN=postgresql://user:password@localhost:5432/book_service_main
DATABASE_URL_SECONDARY=postgresql://user:password@localhost:5432/book_service_secondary
DATABASE_URL_TERTIARY=postgresql://user:password@localhost:5432/book_service_tertiary

# Sharding configuration
SHARDING_BRANCHES=main,secondary,tertiary

# Connection pool settings
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
DATABASE_POOL_TIMEOUT=30

# SQL logging (development only)
SQL_ECHO=false
```

### Database Setup
```bash
# Install dependencies
poetry install

# Create databases
createdb book_service
createdb book_service_main
createdb book_service_secondary
createdb book_service_tertiary

# Run migrations (if using Alembic)
alembic upgrade head
```

## 🚀 Usage Examples

### Basic Setup
```python
from src.infrastructure.database.config import create_tables, create_sharded_tables
from src.infrastructure.database.models import Book, Author

# Create tables in main database
create_tables()

# Create tables in all sharded databases
create_sharded_tables()
```

### Working with Sharded Data
```python
from src.infrastructure.database.sharding import (
    sharding_manager, 
    create_sharded_record, 
    get_sharded_models_for_branch
)

# Get shard for a branch
shard_name = sharding_manager.get_shard_for_branch("branch_001")

# Create a physical exemplar in the correct shard
exemplar = PhysicalExemplar(
    book_id="book_uuid",
    branch_id="branch_001",
    available=True,
    room=1,
    floor=1,
    bookshelf=1,
    created_by="user123",
    updated_by="user123"
)
create_sharded_record("branch_001", exemplar)

# Query all exemplars for a branch
exemplars = get_sharded_models_for_branch("branch_001", PhysicalExemplar)
```

### Cross-Shard Operations
```python
# Execute operation on all shards
def count_exemplars(session):
    return session.query(PhysicalExemplar).count()

results = sharding_manager.execute_on_all_shards(count_exemplars)
total_exemplars = sum(results.values())

# Get branch statistics
stats = sharding_manager.get_branch_statistics("branch_001")
print(f"Branch utilization: {stats['utilization_rate']:.2%}")
```

## 📈 Performance Optimizations

### Indexing Strategy
- **Primary Keys**: UUID with automatic indexing
- **Foreign Keys**: All foreign keys are indexed
- **Composite Indexes**: Branch-specific queries optimized
- **Text Search**: Full-text search capabilities for book titles and descriptions

### Sharding Benefits
- **Horizontal Scaling**: Distribute load across multiple databases
- **Isolation**: Branch-specific data is isolated
- **Performance**: Reduced query complexity per shard
- **Maintenance**: Independent database maintenance per shard

### Connection Pooling
- **Pool Size**: Configurable connection pool (default: 20)
- **Overflow**: Additional connections for peak loads (default: 30)
- **Recycling**: Automatic connection recycling every hour
- **Health Checks**: Connection health monitoring

## 🔒 Data Integrity

### Constraints
- **Foreign Key Constraints**: All relationships have proper constraints
- **Cascade Deletes**: Proper cleanup of related data
- **Unique Constraints**: ISBN codes, composite unique indexes
- **Check Constraints**: Data validation at database level

### Audit Trail
- **Created/Updated Tracking**: All changes tracked with user and timestamp
- **Soft Deletes**: Optional soft delete support
- **Version Control**: Optimistic locking for concurrent updates

## 🧪 Testing

### Running Examples
```bash
cd src/infrastructure/database
python example.py
```

This will:
1. Create all tables in main and sharded databases
2. Insert sample data across shards
3. Demonstrate sharding functionality
4. Show cross-shard query capabilities

### Test Data
The example creates:
- 2 user types (Student, Teacher)
- 2 users (John Doe, Jane Smith)
- 2 authors (Tolkien, Martin)
- 2 book categories (Fantasy, Fiction)
- 2 books (Lord of the Rings, Game of Thrones)
- 2 branches (Main Library, Secondary Library)
- 3 physical exemplars (distributed across shards)
- 2 lending transactions (distributed across shards)

## 📋 Migration Strategy

### Using Alembic
```bash
# Initialize Alembic
alembic init alembic

# Configure for multiple databases
# Edit alembic.ini and env.py for sharding support

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply to main database
alembic upgrade head

# Apply to sharded databases
alembic upgrade head --database=main_shard
alembic upgrade head --database=secondary_shard
alembic upgrade head --database=tertiary_shard
```

### Manual Migration
```python
from src.infrastructure.database.config import engine, sharded_engines
from src.infrastructure.database.models import Base

# Migrate main database
Base.metadata.create_all(bind=engine)

# Migrate sharded databases
for shard_engine in sharded_engines.values():
    Base.metadata.create_all(bind=shard_engine)
```

## 🔍 Monitoring and Maintenance

### Health Checks
```python
# Check database connectivity
def health_check():
    try:
        # Test main database
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        # Test sharded databases
        for shard_name, shard_engine in sharded_engines.items():
            with shard_engine.connect() as conn:
                conn.execute("SELECT 1")
        
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
```

### Performance Monitoring
- **Query Performance**: Monitor slow queries across shards
- **Connection Pool**: Track connection pool utilization
- **Shard Distribution**: Monitor data distribution across shards
- **Branch Statistics**: Track branch-specific metrics

## 🚨 Troubleshooting

### Common Issues
1. **Connection Pool Exhaustion**: Increase pool size or add more shards
2. **Shard Imbalance**: Implement rebalancing strategy
3. **Cross-Shard Queries**: Use aggregation patterns for reporting
4. **Migration Failures**: Ensure all shards are available during migration

### Debug Mode
```bash
# Enable SQL logging
export SQL_ECHO=true

# Run with verbose output
python example.py
```

This setup provides a scalable, performant database architecture that can handle high-volume book management operations with proper data isolation and horizontal scaling capabilities. 