DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "HAVE_A_NICE_DAY",
        "USER":'root',
        "PASSWORD":'931102,ljz',
        "HOST":'127.0.0.1',
        "PORT":'3306'
    }
}

DEFAULT_FILE_STORAGE = "django_cos_storage.TencentCOSStorage"

TENCENTCOS_STORAGE = {
 "BUCKET": "illustration-1305693432",
 "CONFIG": {
     "Region": "ap-chengdu",
    #  "SecretId": "AKIDFIGyRfhW5RrBLPL3at6Ngv8jEg160nW1",
    #  "SecretKey": "Xq16zd6MPIyOn2FG4gFdDaqvocEoDcrt",
    # 子账号密钥
     "SecretId": "AKID1ykJdjfT7cv2va1HKtHSO5ZrvlPr9GB5",
     "SecretKey": "quoY5O9h4FDyd6OTM6f1DG6HFyVovsc9"
 }
}

