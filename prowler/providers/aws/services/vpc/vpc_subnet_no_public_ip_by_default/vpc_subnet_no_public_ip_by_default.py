from prowler.lib.check.models import Check, Check_Report_AWS
from prowler.providers.aws.services.vpc.vpc_client import vpc_client


class vpc_subnet_no_public_ip_by_default(Check):
    def execute(self):
        findings = []
        for vpc in vpc_client.vpcs.values():
            for subnet in vpc.subnets:
                report = Check_Report_AWS(self.metadata())
                report.region = subnet.region
                report.resource_tags = subnet.tags
                report.resource_id = subnet.id
                report.resource_arn = subnet.arn
                if subnet.mapPublicIpOnLaunch:
                    report.status = "FAIL"
                    report.status_extended = (
                        f"VPC subnet {subnet.id} assigns public IP by default."
                    )
                else:
                    report.status = "PASS"
                    report.status_extended = (
                        f"VPC subnet {subnet.id} does NOT assign public IP by default."
                    )
                findings.append(report)

        return findings
