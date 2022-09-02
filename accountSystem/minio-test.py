import minio

minio_conf = {
    'endpoint': '218.31.113.195:9000',
    'access_key': 'sadam',
    'secret_key': 'minio@Sdm98,.',
    'secure': False
}

minioClient = minio.Minio(**minio_conf)


def upload(bucket: str, name: str, fpath: str, content_type: str):
    if not minioClient.bucket_exists(bucket):
        minioClient.make_bucket(bucket_name=bucket)
    resp = minioClient.fput_object(bucket_name=bucket, object_name=name,
                                   file_path=fpath,
                                   content_type=content_type)
    print(resp)
    resp = minioClient.get_presigned_url(method="GET", bucket_name=bucket, object_name=name)
    print(resp)


if __name__ == '__main__':
    upload("images", "minio的初次运行控制台截图", "/Users/shadikesadamu/SLRC/日志/20220815024034.jpg",
           content_type="application/jpeg")
