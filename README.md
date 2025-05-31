# AWS S3 Storage Optimization with Pulumi

Automated lifecycle management for files in S3 with cost-optimized storage transitions.

## Features

- **Automated Storage Tiering**:
  - Immediate access to new uploads (STANDARD)
  - Fast retrieval with Glacier Instant Retrieval after 1 day
  - Cost-effective deep archival after 92 days

- **Infrastructure as Code**:
  - Pulumi Python implementation
  - Configurable transition periods
  - Reproducible deployments

## Lifecycle Flow

```mermaid
graph LR
    A[New Uploads] -->|STANDARD| B[Day 0]
    B -->|GLACIER_IR| C[Day 1]
    C -->|DEEP_ARCHIVE| D[Day 92]
```

## Prerequisites

- Python 3.7+
- Pulumi CLI
- AWS credentials configured
- Unique bucket name

## Configuration

Set required parameters:

```bash
pulumi config set bucket_name "your-unique-bucket-name"
pulumi config set aws:region <your-region>
```

Optional customizations:

```bash
pulumi config set glacier_instant_days 1
pulumi config set deep_archive_days 92
```

## Deployment

1. Initialize the project:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Deploy the infrastructure:

```bash
pulumi up
```

## Architecture

1. **Upload Phase**:
   - Files uploaded to STANDARD storage class
   - Immediate availability for processing

2. **Fast Archive Phase** (Day 1):
   - Transition to GLACIER_IR
   - Millisecond retrieval times
   - 40% cost reduction vs STANDARD

3. **Deep Archive Phase** (Day 92):
   - Transition to DEEP_ARCHIVE
   - Hours retrieval time
   - 95% cost reduction vs STANDARD

## Cost Comparison

| Storage Class | Transition Day | Cost (us-east-1) | Retrieval Time |
|---------------|----------------|------------------|----------------|
| STANDARD | 0 | $0.023/GB | Immediate |
| GLACIER_IR | 1 | $0.004/GB | Milliseconds |
| DEEP_ARCHIVE | 92 | $0.00099/GB | Hours |

## Monitoring

Access monitoring URLs after deployment:

```bash
pulumi stack output monitoring_dashboard_url
```

## Clean Up

To destroy all resources:

```bash
pulumi destroy
```

## Troubleshooting

Common issues:

- **Bucket name not available**: Try a more unique name
- **Transition errors**: Verify days are increasing sequentially
- **Permission issues**: Check IAM credentials

## License

Apache 2.0
```