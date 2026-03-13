            "bucket_name": self.config["bucket_name"],
            "free_tier": self.config["free_tier"],
            "configured": True
        }
    
    def upload_file(self, file_path: str, object_name: Optional[str] = None, 
                   folder: str = "instagram") -> Dict[str, Any]:
        """
        Upload file to R2
        
        Args:
            file_path: Path to file
            object_name: Object name in bucket (optional)
            folder: Folder prefix
            
        Returns:
            Upload result
        """
        try:
            if not object_name:
                object_name = os.path.basename(file_path)
            
            # Add folder prefix
            if folder:
                object_name = f"{folder}/{object_name}"
            
            logger.info(f"📤 Uploading file: {file_path} → {object_name}")
            
            self.s3_client.upload_file(
                file_path,
                self.config["bucket_name"],
                object_name
            )
            
            # Generate public URL
            public_url = f"https://pub-{self.config['account_id']}.r2.dev/{object_name}"
            
            logger.info(f"✅ File uploaded successfully")
            logger.info(f"   Object: {object_name}")
            logger.info(f"   Public URL: {public_url}")
            
            return {
                "success": True,
                "object_name": object_name,
                "public_url": public_url,
                "bucket": self.config["bucket_name"]
            }
            
        except Exception as e:
            logger.error(f"❌ File upload failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_file(self, object_name: str, download_path: str) -> Dict[str, Any]:
        """
        Download file from R2
        
        Args:
            object_name: Object name in bucket
            download_path: Path to save downloaded file
            
        Returns:
            Download result
        """
        try:
            logger.info(f"📥 Downloading: {object_name} → {download_path}")
            
            self.s3_client.download_file(
                self.config["bucket_name"],
                object_name,
                download_path
            )
            
            logger.info(f"✅ File downloaded successfully")
            
            return {
                "success": True,
                "object_name": object_name,
                "download_path": download_path
            }
            
        except Exception as e:
            logger.error(f"❌ File download failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_objects(self, prefix: str = "") -> Dict[str, Any]:
        """
        List objects in bucket
        
        Args:
            prefix: Filter by prefix
            
        Returns:
            List of objects
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.config["bucket_name"],
                Prefix=prefix
            )
            
            objects = response.get('Contents', [])
            
            return {
                "success": True,
                "objects": objects,
                "count": len(objects)
            }
            
        except Exception as e:
            logger.error(f"❌ List objects failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test R2 connection
        
        Returns:
            Test result
        """
        logger.info("🧪 Testing Cloudflare R2 connection...")
        
        try:
            # Try to list buckets (should work with proper permissions)
            response = self.s3_client.list_buckets()
            
            # Check if our bucket exists
            buckets = [b['Name'] for b in response.get('Buckets', [])]
            bucket_exists = self.config["bucket_name"] in buckets
            
            return {
                "success": True,
                "message": "✅ Cloudflare R2 connection successful",
                "bucket_exists": bucket_exists,
                "total_buckets": len(buckets)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection test failed: {e}",
                "suggestion": "Check credentials, bucket exists, and permissions"
            }

# Example usage
if __name__ == "__main__":
    print("🧪 Cloudflare R2 Client Test")
    print("="*50)
    
    try:
        # Initialize client
        client = CloudflareR2Client()
        
        # Show config
        config = client.get_config()
        print(f"✅ Configuration loaded")
        print(f"   Provider: {config['provider']}")
        print(f"   Account ID: {config['account_id']}")
        print(f"   Bucket: {config['bucket_name']}")
        print(f"   Free tier: {config['free_tier']['storage']} storage")
        
        # Test connection
        test_result = client.test_connection()
        if test_result["success"]:
            print(f"✅ {test_result['message']}")
            print(f"   Bucket exists: {test_result.get('bucket_exists', 'N/A')}")
            print(f"   Total buckets: {test_result.get('total_buckets', 'N/A')}")
        else:
            print(f"⚠️  {test_result['error']}")
            print(f"   {test_result.get('suggestion', '')}")
        
        print("\n" + "="*50)
        print("🚀 Cloudflare R2 Client Ready!")
        print("💰 Monthly savings: $50 vs S3/cloud storage")
        print("📊 Free tier: 10GB storage, unlimited requests")
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        print("   Check credentials and configuration")
