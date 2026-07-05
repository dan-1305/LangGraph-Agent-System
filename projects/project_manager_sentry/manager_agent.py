import os
from src.base_agent import BaseAgent
import sqlite3

class ProjectManagerAgent(BaseAgent):
    """
    Agent chuyên trách quản lý Monorepo Metadata và điều phối file.
    Sử dụng SQLite Metadata để tìm kiếm file nhanh chóng, tiết kiệm token.
    """
    
    def __init__(self, name="ProjectSentry", model="gemini-3.1-flash-lite"):
        super().__init__(name, model)
        self.metadata_db = "reports/SYSTEM_MAP_METADATA.db"

    def find_core_files(self, project_name):
        """
        Truy vấn metadata để lấy danh sách core files của một project.
        """
        if not os.path.exists(self.metadata_db):
            return "Metadata DB not found. Run tools/system/project_indexer.py first."
            
        conn = sqlite3.connect(self.metadata_db)
        cursor = conn.cursor()
        
        query = """
        SELECT relative_path FROM project_files 
        JOIN projects ON project_files.project_id = projects.id
        WHERE projects.name = ? AND is_core = 1
        """
        
        cursor.execute(query, (project_name,))
        files = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return files

    def run(self, task):
        # Implementation logic for delegating sub-tasks
        pass
