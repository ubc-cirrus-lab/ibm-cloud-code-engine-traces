# check if 7z is installed
if ! command -v 7z &> /dev/null
then
    echo "7z could not be found, please install it first."
    exit
fi  

# check if the "data" directory exists and if not create it
if [ ! -d "data" ]; then
    mkdir data
fi

# decompress all week_*.7z.001 files 
7z x compressed_data/app_configs.7z
7z x compressed_data/week_1.7z.001
7z x compressed_data/week_2.7z.001
7z x compressed_data/week_3.7z.001
7z x compressed_data/week_4.7z.001
7z x compressed_data/week_5.7z.001
7z x compressed_data/week_6.7z.001
7z x compressed_data/week_7.7z.001
7z x compressed_data/week_8.7z.001
7z x compressed_data/week_9.7z.001
7z x compressed_data/week_10.7z.001

# move all traffic files to the "data" directory
mv week_*.pickle data/
