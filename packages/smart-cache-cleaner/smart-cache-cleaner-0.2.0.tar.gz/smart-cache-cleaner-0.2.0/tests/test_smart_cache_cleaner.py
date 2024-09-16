import unittest
import os
import shutil
import tempfile
import hashlib  # Add this import
from datetime import datetime, timedelta
from src.smart_cache_cleaner.main import (
    scan_directory,
    human_readable_size,
    filter_files,
    delete_file,
    get_cache_and_temp_dirs,
    verify_file_hash
)

class TestSmartCacheCleaner(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Create some test files
        self.test_files = [
            ('file1.txt', 1000, datetime.now() - timedelta(days=1)),
            ('file2.txt', 2000, datetime.now() - timedelta(days=2)),
            ('file3.txt', 3000, datetime.now() - timedelta(days=3)),
        ]
        
        for filename, size, mtime in self.test_files:
            path = os.path.join(self.test_dir, filename)
            with open(path, 'wb') as f:
                f.write(b'0' * size)
            os.utime(path, (mtime.timestamp(), mtime.timestamp()))

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_scan_directory(self):
        scanned_files = list(scan_directory(self.test_dir))
        self.assertEqual(len(scanned_files), 3)
        for scanned, (filename, size, mtime) in zip(scanned_files, self.test_files):
            self.assertEqual(os.path.basename(scanned[0]), filename)
            self.assertEqual(scanned[1], size)
            self.assertAlmostEqual(scanned[2].timestamp(), mtime.timestamp(), delta=1)

    def test_human_readable_size(self):
        self.assertEqual(human_readable_size(1000), "1000.0B")
        self.assertEqual(human_readable_size(1024), "1.0KB")
        self.assertEqual(human_readable_size(1048576), "1.0MB")

    def test_filter_files(self):
        all_files = scan_directory(self.test_dir)
        filtered = list(filter_files(all_files, min_size=1500, max_age=2))
        self.assertEqual(len(filtered), 1)
        self.assertTrue(all(size >= 1500 for _, size, _ in filtered))
        self.assertTrue(all((datetime.now() - mtime).days <= 2 for _, _, mtime in filtered))

    def test_delete_file(self):
        test_file = os.path.join(self.test_dir, 'delete_test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        deleted, success = delete_file(test_file, '')  # Use empty string for hash
        
        self.assertEqual(deleted, test_file)
        self.assertTrue(success)
        self.assertFalse(os.path.exists(test_file))

    def test_get_cache_and_temp_dirs(self):
        dirs = get_cache_and_temp_dirs()
        self.assertIsInstance(dirs, list)
        self.assertTrue(all(os.path.isdir(d) for d in dirs))

    def test_verify_file_hash(self):
        test_file = os.path.join(self.test_dir, 'hash_test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Generate a hash for the file
        with open(test_file, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        # Test with correct hash
        self.assertTrue(verify_file_hash(test_file, file_hash))
        
        # Test with incorrect hash
        self.assertFalse(verify_file_hash(test_file, 'incorrect_hash'))
        
        # Modify the file
        with open(test_file, 'w') as f:
            f.write('modified content')
        
        # Test that the hash no longer matches
        self.assertFalse(verify_file_hash(test_file, file_hash))

if __name__ == '__main__':
    unittest.main()
