# 初學OpenCV

最近因為學校某堂課 Final Project 需要弄手勢辨識，所以先來熟悉OpenCV，以下筆記導向(笑

## Hello world

有包括`highgui` 和 `core`

```cpp
#include <opencv2/highgui/highgui.hpp>

int main(){
    char windowName[] = "HelloWorldWindow";
    cvNamedWindow(windowName, 0x01);

    IplImage* img = cvCreateImage(cvSize(0x96, 0x32), IPL_DEPTH_8U, 0);
    cvSet(img, cvScalar(0xFF, 0xFF, 0xFF));
    
    CvFont font; 
    double hScale = 1, vScale = 1;
    int lineWidth = 1;
    cvInitFont(&font,CV_FONT_HERSHEY_COMPLEX_SMALL|CV_AA,hScale,vScale,0x00,lineWidth);
    
    cvPutText(img, "Hello world", cvPoint(0, 30), &font, cvScalar(0, 0, 0));

    cvShowImage(windowName, img);
    
    cvWaitKey();

    return 0;
}
```

## Video and diff

來源：[OpenCV Error- Assertion failed (dst.data == dst0.data) when converting to grayscale and background subtraction. Please help me! Thank you very much.](http://answers.opencv.org/question/36762/opencv-error-assertion-failed-dstdata-dst0data-when-converting-to-grayscale-and-background-subtraction-please-help-me-thank-you-very-much/)

先是找了個用c-api的code，可是我編譯器是g++，所以遇到Assertion failed的錯誤，翻翻才知道踩到雷。

這個實例應該是對每個Frame做diff，進而得到變化的輪廓。

```cpp
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>

#include <iostream>
using namespace cv;
using namespace std;

int main()
{
    Mat prev;
    VideoCapture cap(0); // 1st cam
    while( cap.isOpened() )
    {
        Mat frame,gray,diff;
        if ( ! cap.read(frame) )
            break;
        imshow("lalala",frame);
        cvtColor( frame, gray, CV_BGR2GRAY );
        if ( ! prev.empty() )
        {
            absdiff( gray, prev, diff );
            imshow("diff",diff);
        }
        prev = gray; // swap
        int k = waitKey(10);
        if ( k==27 )
            break;
    }
    return 0;
}
```

附上makefile:

```makefile
main: main.cpp
	g++ main.cpp `pkg-config --cflags opencv` `pkg-config --libs opencv` -o main
```