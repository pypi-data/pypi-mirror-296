from dipamkara import Dipamkara

database = Dipamkara(
    dimension=1024,
    archive_path=r'E:\Python\Dipamkara\test_archive',
    cached=False
)

print(database.latest_id)
