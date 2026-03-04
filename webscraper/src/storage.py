"""
Storage module for the web scraper.
Saves extracted data to CSV, JSON, and SQLite formats.
"""

import json
import csv
import sqlite3
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.error_handler import StorageError, Logger


class DataStorage:
    """Base class for data storage."""
    
    def __init__(self, output_directory: str = 'output'):
        """
        Initialize data storage.
        
        Args:
            output_directory: Directory to save output files
        """
        self.output_directory = output_directory
        self.logger = Logger()
        os.makedirs(output_directory, exist_ok=True)
    
    def save(self, data: Dict[str, Any], filename: str) -> str:
        """
        Save data (to be implemented by subclasses).
        
        Args:
            data: Data to save
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        raise NotImplementedError


class JSONStorage(DataStorage):
    """Saves data to JSON format."""
    
    def save(self, data: Dict[str, Any], filename: str = 'data.json') -> str:
        """
        Save data to JSON file.
        
        Args:
            data: Data to save
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = os.path.join(self.output_directory, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved to JSON: {filepath}")
            return filepath
        
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {str(e)}")
            raise StorageError(f"Failed to save JSON file: {str(e)}")


class CSVStorage(DataStorage):
    """Saves data to CSV format."""
    
    def save(self, data: Dict[str, Any], filename: str = 'data.csv') -> str:
        """
        Save data to CSV file.
        
        Args:
            data: Data to save
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        try:
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            filepath = os.path.join(self.output_directory, filename)
            
            # Flatten data for CSV format
            flattened_data = self._flatten_data(data)
            
            if not flattened_data:
                self.logger.warning("No data to save to CSV")
                return filepath
            
            # Get all unique keys
            fieldnames = set()
            for item in flattened_data:
                fieldnames.update(item.keys())
            fieldnames = sorted(list(fieldnames))
            
            # Write to CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(flattened_data)
            
            self.logger.info(f"Data saved to CSV: {filepath}")
            return filepath
        
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {str(e)}")
            raise StorageError(f"Failed to save CSV file: {str(e)}")
    
    def _flatten_data(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Flatten nested data for CSV format.
        
        Args:
            data: Nested data dictionary
            
        Returns:
            Flattened list of dictionaries
        """
        flattened = []
        
        for key, items in data.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        row = {'category': key}
                        row.update(item)
                        flattened.append(row)
                    else:
                        flattened.append({'category': key, 'value': str(item)})
            elif isinstance(items, dict):
                row = {'category': key}
                row.update(items)
                flattened.append(row)
            else:
                flattened.append({'category': key, 'value': str(items)})
        
        return flattened


class SQLiteStorage(DataStorage):
    """Saves data to SQLite database."""
    
    def __init__(self, output_directory: str = 'output', db_name: str = 'scraper.db'):
        """
        Initialize SQLite storage.
        
        Args:
            output_directory: Directory to save database
            db_name: Database filename
        """
        super().__init__(output_directory)
        self.db_path = os.path.join(output_directory, db_name)
    
    def save(self, data: Dict[str, Any], table_name: str = 'scraped_data') -> str:
        """
        Save data to SQLite database.
        
        Args:
            data: Data to save
            table_name: Table name to create/insert into
            
        Returns:
            Path to database file
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create metadata table
            self._create_metadata_table(cursor)
            
            # Create data table
            self._create_data_table(cursor, table_name, data)
            
            # Insert data
            self._insert_data(cursor, table_name, data)
            
            # Record metadata
            self._record_metadata(cursor, table_name)
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Data saved to SQLite: {self.db_path}")
            return self.db_path
        
        except Exception as e:
            self.logger.error(f"Error saving to SQLite: {str(e)}")
            raise StorageError(f"Failed to save to SQLite: {str(e)}")
    
    def _create_metadata_table(self, cursor) -> None:
        """Create metadata table if not exists."""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                record_count INTEGER,
                created_at TIMESTAMP,
                UNIQUE(table_name)
            )
        ''')
    
    def _create_data_table(self, cursor, table_name: str, data: Dict[str, Any]) -> None:
        """Create data table based on data structure."""
        # Convert data to flat rows
        rows = self._flatten_data_for_db(data)
        
        if not rows:
            return
        
        # Create table with columns from first row
        columns = rows[0].keys()
        
        create_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        create_sql += 'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        create_sql += ', '.join([f'{col} TEXT' for col in columns])
        create_sql += ')'
        
        cursor.execute(create_sql)
    
    def _insert_data(self, cursor, table_name: str, data: Dict[str, Any]) -> None:
        """Insert data into table."""
        rows = self._flatten_data_for_db(data)
        
        if not rows:
            return
        
        columns = rows[0].keys()
        placeholders = ', '.join(['?' for _ in columns])
        insert_sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        
        for row in rows:
            values = [str(row.get(col, '')) for col in columns]
            cursor.execute(insert_sql, values)
    
    def _record_metadata(self, cursor, table_name: str) -> None:
        """Record metadata about the table."""
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (table_name, record_count, created_at)
            VALUES (?, ?, ?)
        ''', (table_name, count, datetime.now().isoformat()))
    
    def _flatten_data_for_db(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Flatten data for database insertion.
        
        Args:
            data: Nested data dictionary
            
        Returns:
            List of flattened rows
        """
        flattened = []
        
        for key, items in data.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        row = {'category': key}
                        # Flatten nested dicts
                        for k, v in item.items():
                            if isinstance(v, (list, dict)):
                                row[k] = json.dumps(v)
                            else:
                                row[k] = str(v)
                        flattened.append(row)
                    else:
                        flattened.append({'category': key, 'value': str(item)})
            elif isinstance(items, dict):
                row = {'category': key}
                for k, v in items.items():
                    if isinstance(v, (list, dict)):
                        row[k] = json.dumps(v)
                    else:
                        row[k] = str(v)
                flattened.append(row)
            else:
                flattened.append({'category': key, 'value': str(items)})
        
        return flattened


class StorageManager:
    """Manages multiple storage formats."""
    
    def __init__(self, output_directory: str = 'output'):
        """
        Initialize storage manager.
        
        Args:
            output_directory: Directory to save output files
        """
        self.output_directory = output_directory
        self.logger = Logger()
        self.json_storage = JSONStorage(output_directory)
        self.csv_storage = CSVStorage(output_directory)
        self.sqlite_storage = SQLiteStorage(output_directory)
    
    def save(self, data: Dict[str, Any], formats: List[str], prefix: str = '') -> Dict[str, str]:
        """
        Save data in multiple formats.
        
        Args:
            data: Data to save
            formats: List of formats ('json', 'csv', 'sqlite')
            prefix: Prefix for filename
            
        Returns:
            Dictionary mapping format to filepath
        """
        saved_files = {}
        
        for fmt in formats:
            fmt_lower = fmt.lower()
            
            try:
                if fmt_lower == 'json':
                    filename = f'{prefix}data.json' if prefix else 'data.json'
                    filepath = self.json_storage.save(data, filename)
                    saved_files['json'] = filepath
                
                elif fmt_lower == 'csv':
                    filename = f'{prefix}data.csv' if prefix else 'data.csv'
                    filepath = self.csv_storage.save(data, filename)
                    saved_files['csv'] = filepath
                
                elif fmt_lower == 'sqlite':
                    filepath = self.sqlite_storage.save(data)
                    saved_files['sqlite'] = filepath
                
                else:
                    self.logger.warning(f"Unknown format: {fmt}")
            
            except StorageError as e:
                self.logger.error(f"Error saving in {fmt} format: {str(e)}")
                saved_files[fmt_lower] = None
        
        return saved_files
