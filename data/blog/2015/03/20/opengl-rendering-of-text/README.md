# 在OpenGL繪製中文字

在OpenGL裏畫中文字一直是個蛋疼的問題，之前有找過一些Library像是[Freetype GL](https://github.com/rougier/freetype-gl)，但對我的需求來說算滿大的，所以打算自己刻一個小的。

## Freetype-Project

在 **Freetype GL** 也有用到這個，因為要畫字，就需要字形的讀取。

[Documentation](http://www.freetype.org/freetype2/docs/documentation.html)

在Freetype project裡面主要有兩種東西：`FT_Library` 和 `FT_Face`，`FT_Library` 負責把管理字形資料，`FT_Face`負責儲存某個字形的BMP資料。

### FT\_Library 的初始化

```cpp
FT_Libraray ft_lib;
FT_Init_FreeType(ft_lib);
```

### 設定字形

```cpp
FT_Face face;
FT_New_Face(ft_lib, font_path, 0, face);
FT_Set_Char_Size(face, 0, 60 << 6, 96, 96);
```

### 畫字

因為要支援中文字，所以需要 `wchar_t`

```cpp
const wchar_t wstr[20] = L"你我他";
int pen_x = 300, pen_y = 200;
FT_GlyphSlot  slot = face->glyph;  /* a small shortcut */

for(int lx = 0;wstr[lx] != 0; lx++ ){
	FT_Load_Char(face, (unsigned char)wstr[lx], FT_LOAD_RENDER );
	// draw slot->bitmap at (pen_x + slot->bitmap_left, pen_y - slot->bitmap_top);
	pen_x += slot->advance.x >> 6;
}
```

### slot->bitmap

`slot->bitmap`本身是[FT\_Bitmap](http://www.freetype.org/freetype2/docs/reference/ft2-basic_types.html#FT_Bitmap)的結構

```cpp
typedef struct  FT_Bitmap_{
	unsigned int    rows;
	unsigned int    width;
	int             pitch;
	unsigned char*  buffer;
	unsigned short  num_grays;
	unsigned char   pixel_mode;
	unsigned char   palette_mode;
	void*           palette;
} FT_Bitmap;
```

需要的資料是`buffer`、`width`、`rows`，分別是bitmap pixel資料、寬和高


最後弄成這樣的一個小工具：[minftgl](https://github.com/mudream4869/min-ftgl)