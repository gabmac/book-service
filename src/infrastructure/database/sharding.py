"""
Sharding utilities for branch-based database sharding.
"""

import hashlib
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from .config import get_sharded_session, get_branch_shard, sharded_engines


class ShardingManager:
    """Manages database sharding by branch."""
    
    def __init__(self):
        self._branch_cache: Dict[str, str] = {}
    
    def get_shard_for_branch(self, branch_id: str) -> str:
        """Get the shard name for a given branch ID."""
        if branch_id not in self._branch_cache:
            self._branch_cache[branch_id] = get_branch_shard(branch_id)
        return self._branch_cache[branch_id]
    
    def get_session_for_branch(self, branch_id: str) -> Session:
        """Get a database session for a specific branch."""
        shard_name = self.get_shard_for_branch(branch_id)
        return get_sharded_session(shard_name)
    
    def get_all_shards(self) -> List[str]:
        """Get all available shard names."""
        return list(sharded_engines.keys())
    
    def execute_on_all_shards(self, operation):
        """Execute an operation on all shards."""
        results = {}
        for shard_name in self.get_all_shards():
            session = get_sharded_session(shard_name)
            try:
                results[shard_name] = operation(session)
            finally:
                session.close()
        return results
    
    def get_branch_statistics(self, branch_id: str) -> Dict:
        """Get statistics for a specific branch."""
        session = self.get_session_for_branch(branch_id)
        try:
            from .models import PhysicalExemplar, BookLending
            
            # Count physical exemplars
            exemplar_count = session.query(PhysicalExemplar).filter(
                PhysicalExemplar.branch_id == branch_id
            ).count()
            
            # Count available exemplars
            available_count = session.query(PhysicalExemplar).filter(
                PhysicalExemplar.branch_id == branch_id,
                PhysicalExemplar.available == True
            ).count()
            
            # Count active lendings
            active_lendings = session.query(BookLending).filter(
                BookLending.branch_id == branch_id,
                BookLending.returned_at.is_(None)
            ).count()
            
            return {
                "branch_id": branch_id,
                "shard": self.get_shard_for_branch(branch_id),
                "total_exemplars": exemplar_count,
                "available_exemplars": available_count,
                "active_lendings": active_lendings,
                "utilization_rate": (exemplar_count - available_count) / exemplar_count if exemplar_count > 0 else 0
            }
        finally:
            session.close()


# Global sharding manager instance
sharding_manager = ShardingManager()


def get_sharded_models_for_branch(branch_id: str, model_class):
    """Get all records of a model for a specific branch."""
    session = sharding_manager.get_session_for_branch(branch_id)
    try:
        return session.query(model_class).filter(
            getattr(model_class, 'branch_id') == branch_id
        ).all()
    finally:
        session.close()


def create_sharded_record(branch_id: str, model_instance):
    """Create a record in the appropriate shard for a branch."""
    session = sharding_manager.get_session_for_branch(branch_id)
    try:
        session.add(model_instance)
        session.commit()
        return model_instance
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_sharded_record(branch_id: str, model_class, record_id: str, **updates):
    """Update a record in the appropriate shard for a branch."""
    session = sharding_manager.get_session_for_branch(branch_id)
    try:
        record = session.query(model_class).filter(
            model_class.id == record_id,
            getattr(model_class, 'branch_id') == branch_id
        ).first()
        
        if not record:
            raise ValueError(f"Record {record_id} not found in branch {branch_id}")
        
        for key, value in updates.items():
            setattr(record, key, value)
        
        session.commit()
        return record
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_sharded_record(branch_id: str, model_class, record_id: str):
    """Delete a record from the appropriate shard for a branch."""
    session = sharding_manager.get_session_for_branch(branch_id)
    try:
        record = session.query(model_class).filter(
            model_class.id == record_id,
            getattr(model_class, 'branch_id') == branch_id
        ).first()
        
        if not record:
            raise ValueError(f"Record {record_id} not found in branch {branch_id}")
        
        session.delete(record)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close() 