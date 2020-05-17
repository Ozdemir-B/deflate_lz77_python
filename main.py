from skalg import *


lz=lz77().encode("metin.txt",300,100)
#encode("file.txt",search buffer size, look ahead buffer size)
#you need to decompress the file_encoded file
#file_encoded_txt.txt file shows the compressed file
#returns an array of tuples [(offset,lenght,character)]


lz77().decode("metin_encoded.txt")
#decode("file_encoded") creates file_encoded_decoded.txt which is the reconstructed text




deflate().encode("metin.txt",300,100)
#encode("file.txt",search buffer size,look ahead buffer size)
#creates file_deflated.txt file. which is the compressed form of the file
#also creates file_key_o.txt and file_key_s.txt to reconstruct the compressed data


deflate().decode("metin_deflated.txt","metin_key_o.txt","metin_key_s.txt")
#decode("file_deflated.txt","file_key.txt")
#uses file_key_o.txt and file_key_s.txt as the key for huffman decoding
#creates file_deflated_unhuffed as the reconstructed lz77 form of the file
#creates file_deflated_unhuffed_encoded.txt as the reconstructed file
