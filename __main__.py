import pulumi
from pulumi_aws import s3

# Configuration with default values
config = pulumi.Config()
bucket_name = config.require("bucket_name")
glacier_instant_days = config.get_int("glacier_instant_days") or 1
deep_archive_days = config.get_int("deep_archive_days") or 92

# Create S3 bucket with optimized lifecycle rules
bucket = s3.Bucket(bucket_name,
    bucket=bucket_name,
    acl="private",
    lifecycle_rules=[
        s3.BucketLifecycleRuleArgs(
            enabled=True,
            transitions=[
                # Standard -> Glacier Instant Retrieval (1 day)
                s3.BucketLifecycleRuleTransitionArgs(
                    days=glacier_instant_days,
                    storage_class="GLACIER_IR"
                ),
                # Standard-IA -> Deep Archive (92 days)
                s3.BucketLifecycleRuleTransitionArgs(
                    days=deep_archive_days,
                    storage_class="DEEP_ARCHIVE"
                )
            ],
            abort_incomplete_multipart_upload_days=7
        )
    ]
)

# Export the bucket details
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
