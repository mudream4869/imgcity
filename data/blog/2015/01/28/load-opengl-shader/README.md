# 載入OpenGL Shader

在想CRPG的紅線問題是否能用shader解決，就來看看shader怎用怎寫．
在網路上東湊西湊 終於湊出一個完整的code

以下是測試用的code，資源沒好好回收請見諒

* main.cpp

```c++
#include <OpenGL/gl.h> 
#include <OpenGL/glu.h> 
#include <GLUT/glut.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
using namespace std;

std::vector<char*> GetFile(const char* path){
    std::vector<char*> ret;
    char gl[1000];
    FILE* fp = fopen(path, "r");
    while(fgets(gl, 100, fp) != NULL){
        char* new_ptr = new char[strlen(gl) + 2];
        strcpy(new_ptr, gl);
        ret.push_back(new_ptr);
    }
    return ret;
}


void LoadShader(){
    auto v_shader = glCreateShader(GL_VERTEX_SHADER);
    
    auto get_vp = GetFile("text.vp");
    int* v_cnt = new int[get_vp.size()];
    for(int lx = 0;lx < get_vp.size();lx++)
        v_cnt[lx] = strlen(get_vp[lx]);
    glShaderSource(v_shader, get_vp.size(), &get_vp[0], v_cnt);
    glCompileShader(v_shader);
   
    auto f_shader = glCreateShader(GL_FRAGMENT_SHADER);
    
    
    auto get_fp = GetFile("text.fp");
    int* f_cnt = new int[get_fp.size()];
    for(int lx = 0;lx < get_fp.size();lx++)
        f_cnt[lx] = strlen(get_fp[lx]);
    glShaderSource(f_shader, get_fp.size(), &get_fp[0], f_cnt);
    glCompileShader(f_shader);
    
    GLuint program = glCreateProgram();
    glAttachShader(program, v_shader);
    glAttachShader(program, f_shader);
    glLinkProgram(program);  
    glUseProgram(program);
    
    return;
}

void Render(){
    glClear( GL_COLOR_BUFFER_BIT );

    glLoadIdentity();

    //Solid cyan quad in the center
    glTranslatef( 100/2.f, 100/ 2.f, 0.f );
    glBegin( GL_QUADS );
    glColor3f( 0.f, 1.f, 1.f );
    glVertex2f( -50.f, -50.f );
    glVertex2f(  50.f, -50.f );
    glVertex2f(  50.f,  50.f );
    glVertex2f( -50.f,  50.f );
    glEnd();

    //Update screen
    glutSwapBuffers();
    return;
}

int main(int argc, char* argv[]){
    glutInit(&argc, argv);
    glutInitWindowSize(600, 600);
    glutCreateWindow("test render");
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_ALPHA); 

    glutDisplayFunc(Render);
    glEnable(GL_BLEND);
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    LoadShader();
 
    glutMainLoop();

    return 0;
}
```

* text.vp

```c++
void main(){
    gl_Position = gl_Vertex;
}
```

* text.fp

```c++
void main(){
    float x = sin(gl_FragCoord.x);
    float y = sin(gl_FragCoord.y);
    float z = sin(gl_FragCoord.z);
    gl_FragColor = vec4(x, y, z, 1.0);
}
```