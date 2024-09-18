def resolve_zkteco_codes(codes_list, value):
    for entry in codes_list:
        if entry[0] == value:
            return entry[1]
    return None


def normalize_pin(pin):
    return pin.lstrip('0')
    
def detect_image_format(src_img):
    # Maps only the 6 first bits of the base64 data, accurate enough
    # for our purpose and faster than decoding the full blob first
    FILETYPE_BASE64_MAGICWORD = {
        b'/': 'JPEG',
        b'R': 'gif',
        b'i': 'PNG',
        b'P': 'svg+xml',
    }

    return FILETYPE_BASE64_MAGICWORD.get(src_img[:1], 'JPEG')

import hashlib

def debug_image_data(data):
    # Print the size of the data in bytes
    data_size = len(data)
    print(f"Data size: {data_size} bytes")

    # Generate an MD5 hash of the data and print the first 10 characters
    hash_value = hashlib.md5(data).hexdigest()
    short_hash = hash_value[:10]  # Taking the first 10 characters of the hash
    print(f"Data hash (first 10 chars): {short_hash}")
    
    first_100_chars = data[:100]
    print(f"First 100 bytes of data: {first_100_chars}")
    
    # Print the last 100 characters of the data
    last_100_chars = data[-100:]
    print(f"Last 100 bytes of data: {last_100_chars}")

    # Find differences between first and last 100 bytes for quick analysis
    # diffs = [(i, first, last) for i, (first, last) in enumerate(zip(first_100_chars, last_100_chars)) if first != last]
    # if diffs:
    #     print("Differences between first and last 100 bytes:")
    #     for i, first, last in diffs:
    #         print(f"Position {i}: First part byte = {first}, Last part byte = {last}")
    # else:
    #     print("No differences found between the first and last 100 bytes.")



def zkteco_to_file(src_img, filename):
    if isinstance(src_img, str):
        import base64
        src_img = base64.b64decode(src_img)
    debug_image_data(src_img)
    with open(filename, 'wb') as f:
        f.write(src_img)
    

def zkteco_format_image(src_img):
    import base64
    from PIL import Image
    import io
    dst_img = base64.b64decode(src_img)
    try:
        image_type = detect_image_format(src_img)
    except:
        image_type = 'PNG'
        
    if image_type == 'JPEG':
        # zkteco_to_file(src_img, "zkteco_format_image.jpg")
        dst_img = src_img.decode('utf-8')
    else:
        # zkteco_to_file(src_img, "zkteco_format_image.png")
        image = Image.open(io.BytesIO(dst_img))
        # Convertir l'image en JPEG
        with io.BytesIO() as buffer:
            image.convert('RGB').save(buffer, format="JPEG")
            jpg_img = buffer.getvalue()
        dst_img = base64.b64encode(jpg_img).decode('utf-8')

    # zkteco_to_file(dst_img, "zkteco_format_image.jpg")
    return dst_img