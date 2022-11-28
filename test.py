import requests
import base64
import chardet


ProfilePicture = requests.get("http://127.0.0.1:3000/GetUserPicture/222533880", "utf-8")

#the_encoding = chardet.detect(ProfilePicture.text)["encoding"]

# print(the_encoding)

ProfilePictureBytes = (ProfilePicture.text).encode("utf-16")

base64_image = base64.encodebytes(ProfilePictureBytes).hex()

# print(base64_image)


from robohash import Robohash
import chardet


def CreateProfilePicture(hash):
    path = "E:\Programowanie\Projekty\RPS-Client\static\profilePictures\\"
    rh = Robohash(hash)
    rh.assemble(roboset="set1")
    
    rh = bytearray(rh)
    the_encoding = chardet.detect(rh)["encoding"]
    print(the_encoding)
    with open(path + hash + "ProfilePicture" + ".png", "wb") as f:
        rh.img.save(f, format="png")

    # Convert digital data to binary format
    with open(path + hash + "ProfilePicture" + ".png", "rb") as file:
        binaryData = file.read()
    return binaryData


CreateProfilePicture("Maciej")
