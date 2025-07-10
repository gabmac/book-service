# Book Service

## Business Summary

**Book Service** is a comprehensive library management system designed to streamline book catalog operations and physical inventory management across multiple library branches. The system serves as the backbone for library operations, enabling librarians and administrators to efficiently manage their book collections, track physical inventory, and maintain detailed catalog information.

### Core Business Objectives

- **Centralized Book Management**: Maintain a comprehensive catalog of books with detailed metadata including ISBN codes, editions, authors, categories, and publication information
- **Multi-Branch Inventory Tracking**: Track physical book exemplars across different library branches with precise location information (room, floor, bookshelf)

## Database Schema

The system uses a PostgreSQL database with a well-structured relational schema designed for scalability and data integrity. All entities inherit from a base model with common audit fields (id, created_at, updated_at, created_by, updated_by).

```mermaid
erDiagram
    AUTHOR {
        UUID id PK
        string name
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    BOOK {
        UUID id PK
        string isbn_code
        string editor
        int edition
        BookType type
        date publish_date
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    BOOK_CATEGORY {
        UUID id PK
        string title
        string description
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    BOOK_DATA {
        UUID id PK
        string language
        string summary
        string title
        UUID book_id FK
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    BRANCH {
        UUID id PK
        string name
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    PHYSICAL_EXEMPLAR {
        UUID id PK
        boolean available
        int room
        int floor
        int bookshelf
        UUID book_id FK
        UUID branch_id FK
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    AUTHOR_BOOK_LINK {
        UUID id PK
        UUID author_id FK
        UUID book_id FK
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    BOOK_BOOK_CATEGORY_LINK {
        UUID id PK
        UUID book_id FK
        UUID book_category_id FK
        datetime created_at
        datetime updated_at
        string created_by
        string updated_by
    }

    %% Relationships
    AUTHOR ||--o{ AUTHOR_BOOK_LINK : "has"
    BOOK ||--o{ AUTHOR_BOOK_LINK : "written by"

    BOOK ||--o{ BOOK_BOOK_CATEGORY_LINK : "belongs to"
    BOOK_CATEGORY ||--o{ BOOK_BOOK_CATEGORY_LINK : "contains"

    BOOK ||--o{ BOOK_DATA : "has translations/data"
    BOOK ||--o{ PHYSICAL_EXEMPLAR : "has copies"
    BRANCH ||--o{ PHYSICAL_EXEMPLAR : "stores"
```

### Entity Descriptions

- **Author**: Stores author information with indexed name field for efficient searching
- **Book**: Core entity containing book metadata (ISBN, editor, edition, type, publish date)
- **BookCategory**: Categorization system with unique titles for organizing books
- **BookData**: Multi-language support and additional book information (title translations, summaries)
- **Branch**: Library branch information for multi-location management
- **PhysicalExemplar**: Physical book tracking with precise location data (room, floor, bookshelf) and availability status
- **AuthorBookLink**: Many-to-many relationship between authors and books
- **BookBookCategoryLink**: Many-to-many relationship between books and categories

### Key Design Features

- **UUID Primary Keys**: Ensures global uniqueness and security
- **Audit Trail**: All entities track creation and modification timestamps with user attribution
- **Cascade Deletion**: Physical exemplars and book data are automatically removed when parent books are deleted
- **Indexed Fields**: Strategic indexing on frequently queried fields (author names, book titles, foreign keys)
- **Data Integrity**: Foreign key constraints maintain referential integrity across all relationships
