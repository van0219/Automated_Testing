"""
Test script for TES-070 generator

This demonstrates how to use the generator to create a TES-070 document
"""

from tes070_generator import generate_tes070, TES070Data, TestScenario, TestStep

# Create sample test data
data = TES070Data(
    client_name="State of New Hampshire",
    interface_id="INT_TEST_001",
    interface_name="Sample Test Interface",
    author="Kiro AI Assistant",
    environment="ACUITY_TST",
    user_roles=["Process Server Administrator", "Financials Processor"],
    test_data_requirements="Sample test files in FSM format",
    configuration_prerequisites="File Channel configured and active",
    scenarios=[
        TestScenario(
            title="Scenario: Successful Interface Processing",
            description="This scenario tests the happy path where all data is valid and processes successfully.",
            test_steps=[
                TestStep(
                    number="1",
                    description="Drop test file to SFTP server",
                    result="PASS"
                ),
                TestStep(
                    number="2",
                    description="Verify File Channel scans and processes file",
                    result="PASS"
                ),
                TestStep(
                    number="3",
                    description="Check staging data imported correctly",
                    result="PASS"
                ),
                TestStep(
                    number="4",
                    description="Verify work unit completed successfully",
                    result="PASS"
                )
            ],
            results=[
                "File successfully processed",
                "All records imported to staging",
                "Work unit completed without errors",
                "Email notification sent to users"
            ],
            screenshots=[]  # Add screenshot paths here
        ),
        TestScenario(
            title="Scenario: Error Handling",
            description="This scenario tests error detection and reporting when invalid data is submitted.",
            test_steps=[
                TestStep(
                    number="1",
                    description="Drop file with invalid data to SFTP",
                    result="PASS"
                ),
                TestStep(
                    number="2",
                    description="Verify errors are detected",
                    result="PASS"
                ),
                TestStep(
                    number="3",
                    description="Check error notification sent",
                    result="PASS"
                )
            ],
            results=[
                "Errors correctly identified",
                "Error notification sent with details",
                "Invalid records not processed"
            ],
            screenshots=[]
        )
    ]
)

# Generate the document
output_path = "TES-070/Generated_TES070s/Sample_Test_Results.docx"
result = generate_tes070(data, output_path)

print(f"\n✅ Test document generated successfully!")
print(f"📄 Location: {result}")
print(f"\n📊 Summary:")
print(f"   Scenarios: {len(data.scenarios)}")
print(f"   Total Tests: {data.total_tests}")
print(f"   Passed: {data.passed_tests}")
print(f"   Pass Rate: {data.percent_passed}")
