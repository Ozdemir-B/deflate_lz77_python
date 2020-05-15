# deflate_lz77_python
python implamentation for deflate and lz77 text compression algorithms

lz77().encode("file.txt",int searchBufferSize, int lookAheadBufferSize)
**creates a compressed form of file.txt named as file_encoded
**also creates file_encoded_txt.txt to examine the compressed form
**returns a list of tuple which is compressed form of the file
 
 lz77().decode("file_encoded")
 **reconstructs the file_encoder named as file_encoded_decoded.txt

deflate().encode("file.txt",int searchBufferSize, int lookAheadBufferSize)
**creates a deflated form of the "file.txt named as "file_deflated.txt"
**creates file_key_o.txt and file_key_s.txt as the keys to reconstruct the data later.

deflate().decode("file_deflated.txt","file_key_o.txt","file_key_s.txt")
**creates file_deflated_unhuffed as part of the reconstruction process, which is also lz77 compressed form of the file.txt
**creates "file_deflated_unhuffed_decoded.txt" as the final reconstructed form of the deflated file.
 
