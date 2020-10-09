# OpenAL 簡易教學

要使用`OpenAL`，首先要知道裡面的四個東西：

* context: 要播放聲音的地方，可以想成`OpenGL`裡面的Window
* listener: `OpenAL` 支援3D音效，所以聽者的資訊是很重要的
* sources: 聲源的資訊
* buffer: 負責聲源的內容

首先是要將一個聲音檔讀入，以下示範wav檔案：

## WAV檔案

其實alut裡面有一個函數可以讀取，可是alut需要額外裝，加上我第一次試驗的code前前後後就只有這一個函數用到alut，所以就來研究一下要如何不靠alut把wav檔案讀入．

### WAV檔案格式

WAV是binary檔，主要有三個區塊：

#### RIFF Header


[WIKI: RIFF Header](http://zh.wikipedia.org/wiki/Resource_Interchange_File_Format)

| Name          | Size  | Type     |
| ------------- |:-----:|:--------:|
| ChunkID       | 4     | char * 4 |
| ChunkSize     | 4     | int * 1  | 
| Format        | 4     | char * 4 |

* ChunkID 必須是 `"RIFF"`
* Format 必須是 `"WAVE"`

```cpp
struct RIFF_Header {
    char chunkID[4];
    int chunkSize;//size not including chunkSize or chunkID
    char format[4];
};
```

#### WAVE 格式 + 資料

| Name             | Size  | Type           |
| ---------------- |:-----:|:--------------:|
| subChunk1ID      | 4     | char * 4       |
| subChunk1Size    | 4     | int * 1        | 
| audio Format     | 2     | short * 1      |
| num Channel      | 2     | short * 1      |
| Sample Rate      | 4     | int * 1        |
| Byte Rate        | 4     | int * 1        |
| Byte Align       | 2     | short * 1      |
| bits Per Sample  | 2     | short * 1      |
| subChunk2ID      | 4     | int * 1        |
| subChunk2Size    | 4     | int * 1        |
| Data             |       | unsigned char  |

```cpp
struct WAVE_Format {
    char subChunkID[4];
    int subChunkSize;
    short audioFormat;
    short numChannels;
    int sampleRate;
    int byteRate;
    short blockAlign;
    short bitsPerSample;
};

struct WAVE_Data {
    char subChunkID[4]; //should contain the word data
    int subChunk2Size; //Stores the size of the data block
};
```

在設定`OpenAL`的聲音format時會需要考慮`num Channel`, `bits per Sample`

以上是WAV格式簡略的介紹，接下來就是OpenAL的部分

## OpenAL簡略的播放聲音

首先是初始化，像在前面有提過的，有device和context

```cpp
ALCdevice* dev = alcOpenDevice(NULL);
ALCcontext* ctx = alcCreateContext(dev, NULL);
alcMakeContextCurrent(ctx);
```

Listener 的初始化：

```cpp
ALfloat listenerPos[]={0.0,0.0,4.0};
ALfloat listenerVel[]={0.0,0.0,0.0};
ALfloat listenerOri[]={0.0,0.0,1.0, 0.0,1.0,0.0};
alListenerfv(AL_POSITION,listenerPos);
alListenerfv(AL_VELOCITY,listenerVel);
alListenerfv(AL_ORIENTATION,listenerOri);
```

### 準備WavLoader

首先比較特別的是我們需要決定好format
```cpp
if (wave_format.numChannels == 1) {
    if (wave_format.bitsPerSample == 8 )
        *format = AL_FORMAT_MONO8;
    else if (wave_format.bitsPerSample == 16)
        *format = AL_FORMAT_MONO16;
} else if (wave_format.numChannels == 2) {
    if (wave_format.bitsPerSample == 8 )
        *format = AL_FORMAT_STEREO8;
    else if (wave_format.bitsPerSample == 16)
        *format = AL_FORMAT_STEREO16;
}
```


```cpp
bool loadWavFile(const char* filename, 
    ALuint* buffer, ALsizei* size, ALsizei* frequency, ALenum* format) {
    fprintf(stderr, "[1] filename = %s\n", filename);
    FILE* soundFile = NULL;
    WAVE_Format wave_format;
    RIFF_Header riff_header;
    WAVE_Data wave_data;
    unsigned char* data = 0;

    soundFile = fopen(filename, "rb");
    // Read in the first chunk into the struct
    fread(&riff_header, sizeof(RIFF_Header), 1, soundFile);
    
    //Read in the 2nd chunk for the wave info
    fread(&wave_format, sizeof(WAVE_Format), 1, soundFile);
    
    //check for extra parameters;
    if (wave_format.subChunkSize > 16)
        fseek(soundFile, sizeof(short), SEEK_CUR);

    //Read in the the last byte of data before the sound file
    fread(&wave_data, sizeof(WAVE_Data), 1, soundFile);
        
    //Allocate memory for data
    data = new unsigned char[wave_data.subChunk2Size];
    fread(data, wave_data.subChunk2Size, 1, soundFile);
        
    //Now we set the variables that we passed in with the
    //data from the structs
    *size = wave_data.subChunk2Size;
    *frequency = wave_format.sampleRate;
    //The format is worked out by looking at the number of
    //channels and the bits per sample.
    if (wave_format.numChannels == 1) {
        if (wave_format.bitsPerSample == 8 )
            *format = AL_FORMAT_MONO8;
        else if (wave_format.bitsPerSample == 16)
            *format = AL_FORMAT_MONO16;
    } else if (wave_format.numChannels == 2) {
        if (wave_format.bitsPerSample == 8 )
            *format = AL_FORMAT_STEREO8;
        else if (wave_format.bitsPerSample == 16)
            *format = AL_FORMAT_STEREO16;
    }
    
    //create our openAL buffer and check for success
    alGenBuffers(1, buffer);
    alBufferData(*buffer, *format, (void*)data, *size, *frequency);
    //clean up and return true if successful
    fclose(soundFile);
    fprintf(stderr, "load ok\n");
    delete[] data;
    return true;
}
```

然後就可以播放拉，先把buffer讀取進來，指定給source，然後播放．

```cpp
alGenSources(1, &source);
loadWavFile("Under_Water.wav", buffer, &size, &freq, &format);
alSourcef(source, AL_PITCH, 1.0f);
alSourcef(source, AL_GAIN, 1.0f);
alSourcefv(source, AL_POSITION, source0Pos);
alSourcefv(source, AL_VELOCITY, source0Vel);
alSourcei(source, AL_BUFFER, buffer[0]);
alSourcePlay(source);  
```

## 完整code(包括多重播放)

[Gist:altest1.cpp](https://gist.github.com/mudream4869/34541dfbd12a747b027e)

## 參考資料

1. [Tutorial: Loading Wave files in OpenAL without ALUT](http://www.dunsanyinteractive.com/blogs/oliver/?cat=16)
1. [Play Compressed Formats With OpenAL](http://kcat.strangesoft.net/openal-tutorial.html)
1. [Creative OpenAL Programmer’s Reference](http://open-activewrl.sourceforge.net/data/OpenAL_PGuide.pdf)
1. [OpenAL Tutorial 1 - Playing WAV files (No ALUT required!)](http://enigma-dev.org/forums/index.php?topic=730.0;wap2)