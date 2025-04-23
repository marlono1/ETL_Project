import great_expectations as gx
import os


def get_context():
    os.environ["GX_CLOUD_ACCESS_TOKEN"] = "25b7e5461b2d462dbe60ea0cf5190985.V1.TSywhrJ59vVVG1He7ODEDCZ8UYO9gF3OjnXa-1k7d2rM-vSakTtT5zeXCY0bE3ttlclOvQcneycPxKKJNqCwpg"
    os.environ["GX_CLOUD_ORGANIZATION_ID"] = "6b1c08b2-881c-403c-9859-cf32e073386f"
    
    context = gx.get_context(cloud_mode=True)   # sets script to run in ram memory and since data is stored in GX cloud
    return context
      