import unittest
import tempfile
import shutil
import pandas as pd
from pathlib import Path
from dmf.io import compress, decompress

class TestCompression(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.sub_test_dir = Path(self.test_dir) / "subdir"
        self.input_file = Path(self.test_dir) / "test.csv"
        self.df = pd.DataFrame({"a": [1, 2, 3]})
        self.df2 = pd.DataFrame({"b": [4, 5, 6]})
        

    def tearDown(self):
        # Remove the temporary directory and all its contents
        shutil.rmtree(self.test_dir)

    def test_compression_decompression_file(self):
        compression_formats = [
            "gz", "gzip", "bz2", "bzip2", "xz", 
            "zip", "7z", "tar", "tgz", 
            "tar.gz", "tar.bz2", "tar.xz"
        ]

        for compression in compression_formats:
            with self.subTest(compression=compression):

                self.df.to_csv(self.input_file, index=False)
                
                # Compress the input file
                output_dir = compress(self.input_file, compression=compression)
                target_dir = self.input_file.with_suffix(f".csv.{compression}")

                self.assertTrue(target_dir.exists())
                self.assertEqual(output_dir, target_dir)
                self.input_file.unlink()

                # Decompress the file
                decompress(output_dir, output_dir=self.test_dir, compression=compression)
                output_dir.unlink()
                #self.assertEqual(restored_dir, self.input_file)
                self.assertTrue(pd.read_csv(self.input_file).equals(self.df))
                self.input_file.unlink()
                # Assert test_dir is empty
                self.assertFalse(list(Path(self.test_dir).iterdir()))

    def test_compression_decompression_folder(self):
        compression_formats = [
            "zip", "7z", "tar", "tgz", 
            "tar.gz", "tar.bz2", "tar.xz"
        ]
        for compression in compression_formats:
            with self.subTest(compression=compression):
                self.test_dir = tempfile.mkdtemp()
                self.sub_test_dir = Path(self.test_dir) / "subdir"
                self.input_file = Path(self.test_dir) / "test.csv"
                self.input_file2 = Path(self.test_dir) / "test2.csv"

                # Create subdir and save two CSV files in it
                self.sub_test_dir.mkdir(exist_ok=True)
                file1 = self.sub_test_dir / "test1.csv"
                file2 = self.sub_test_dir / "test2.csv"
                self.df.to_csv(file1, index=False)
                self.df2.to_csv(file2, index=False)

                # Compress the folder
                output_file = compress(self.sub_test_dir, compression=compression)
                target_file = self.sub_test_dir.with_suffix(f".{compression}")                

                self.assertTrue(target_file.exists())
                self.assertEqual(output_file, target_file)

                # Remove the original directory
                shutil.rmtree(self.sub_test_dir)

                #print(list(os.walk(self.test_dir)))

                # Decompress the folder
                decompress(target_file, output_dir=self.test_dir, compression=compression)
                target_file.unlink()
                
                # Check if the decompressed files match the original data
                restored_file1 = self.sub_test_dir / "test1.csv"
                restored_file2 = self.sub_test_dir / "test2.csv"

                self.assertTrue(restored_file1.exists(), f"{restored_file1} does not exist")
                self.assertTrue(restored_file2.exists(), f"{restored_file2} does not exist")

                self.assertTrue(pd.read_csv(restored_file1).equals(self.df))
                self.assertTrue(pd.read_csv(restored_file2).equals(self.df2))

                # # Clean up after the subtest
                shutil.rmtree(self.test_dir)
                
            self.test_dir = tempfile.mkdtemp()

    def test_compression_decompression_password(self):
        # Only ZIP and 7z formats support passwords
        compression_formats = ["7z"]
        password = "testpassword"

        for compression in compression_formats:
            with self.subTest(compression=compression):
                self.df.to_csv(self.input_file, index=False)
                
                # Compress the input file with a password
                compress(self.input_file, compression=compression, password=password)
                target_file = self.input_file.with_suffix(f".csv.{compression}")

                # Check that the compressed file exists
                self.assertTrue(target_file.exists())

                # Remove the original file to ensure it's restored from the compressed file
                self.input_file.unlink()

                # Decompress the file using the correct password
                decompress(target_file, output_dir=self.test_dir, compression=compression, password=password)
                target_file.unlink()

                # Verify that the decompressed file matches the original data
                self.assertTrue(pd.read_csv(self.input_file).equals(self.df))

                # Clean up after the subtest
                self.input_file.unlink()
                # Assert that test_dir is empty
                self.assertFalse(list(Path(self.test_dir).iterdir()))


    def test_compression_decompression_password_invalid(self):
        # Only ZIP and 7z formats support passwords
        compression_formats = ["7z"]
        password = "testpassword"

        for compression in compression_formats:
            for pwd in [None, "invalidpassword"]:
                with self.subTest(compression=compression, pwd=pwd):
                    self.df.to_csv(self.input_file, index=False)
                    
                    # Compress the input file with a password
                    compress(self.input_file, compression=compression, password=password)
                    target_file = self.input_file.with_suffix(f".csv.{compression}")

                    # Check that the compressed file exists
                    self.assertTrue(target_file.exists())

                    # Remove the original file to ensure it's restored from the compressed file
                    self.input_file.unlink()

                    # Decompress the file using the correct password
                    with self.assertRaises(Exception):
                        decompress(target_file, output_dir=self.test_dir, compression=compression, password=pwd)

                    target_file.unlink()
                    self.input_file.unlink()

                    # Assert that test_dir is empty
                    self.assertFalse(list(Path(self.test_dir).iterdir()))

    def test_compression_folder_not_supported(self):
        compression_formats = ["gz", "gzip", "bz2", "bzip2", "xz"]
        self.sub_test_dir = Path(self.test_dir) / "subdir"
        self.sub_test_dir.mkdir(exist_ok=True)
        self.df.to_csv(self.sub_test_dir / "test.csv", index=False)

        for compression in compression_formats:
            with self.subTest(compression=compression):
                with self.assertRaises(ValueError):
                    compress(self.sub_test_dir, compression=compression)

    def test_password_not_supported(self):
        compression_formats = ["zip", "tar", "tgz", "tar.gz", "tar.bz2", "tar.xz"]
        self.df.to_csv(self.input_file, index=False)

        for compression in compression_formats:
            with self.subTest(compression=compression):
                with self.assertRaises(NotImplementedError):
                    compress(self.input_file, compression=compression, password="testpassword")
            

if __name__ == "__main__":
    unittest.main()
