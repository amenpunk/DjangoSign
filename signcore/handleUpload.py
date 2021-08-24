def handle_uploaded_file(f):
    print(f"file to uploadl {f}")
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
