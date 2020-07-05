Lumen Pinyin (Guāngyào Pīnyīn 光耀拼音)
===
Lumen Pinyin (Guāngyào Pīnyīn 光耀拼音) is an input schema for [Rime](https://rime.im/) that can be used to type [pinyin](https://en.wikipedia.org/wiki/Pinyin). It works similarly to existing pinyin-based input methods, except it's built for typing Standard Chinese in [pinyin orthography](http://pinyin.info/readings/zyg/rules.html) instead of Chinese characters.

Lumen Pinyin is named after [Zhou Youguang](https://en.wikipedia.org/wiki/Zhou_Youguang) 周有光, the inventor of pinyin. Both his given name Yàopíng 耀平 (“brilliant peace”) and his pen name Yǒuguāng 有光 (“with light”) are related to light (*lūmen* in Latin), and characters from his names combine to form the word guāngyào 光耀, “brilliance”.

Installation
---
This installation process is gathered and translated from the official Rime documentation, which is mostly in Chinese. I've linked the original instructions from which I've taken each of these steps. If you run into any issues, feel free to contact me at `<wpan@berkeley.edu>`. 

1. Install Rime. The easiest way to do this is to download the package for your operating system from [their website](https://rime.im/) (blue button) and click through the installation process. 
2. Follow the English instructions [here](https://github.com/rime/plum#usage) to set up Rime's configuration manager, `plum` (東風破), then install Lumen Pinyin by running `bash rime-install williampan/rime-lumen-pinyin` from within the `plum` folder.
   
    Alternatively, manually download `lumen_pinyin.dict.yaml` and `lumen_pinyin.schema.yaml` from this repository and copy them into the Rime configuration folder. This folder is located at: 
    * Mac: `~/Library/Rime/`
    * Windows: `"%APPDATA%\Rime"`
    * Linux: `~/.config/ibus/rime/` 

    ([Chinese instructions](https://github.com/rime/home/wiki/RimeWithSchemata#rime-%E4%B8%AD%E7%9A%84%E6%95%B8%E6%93%9A%E6%96%87%E4%BB%B6%E5%88%86%E4%BD%88%E5%8F%8A%E4%BD%9C%E7%94%A8))

    
3. In the configuration folder (listed above), find the file named `default.yaml` and open it in a text editor. Find and copy the whole `schema_list` section:
    ```
    schema_list: 
      - schema: luna_pinyin
      # possible additional schema entries here 
    ```
    Then make a new file called `default.custom.yaml` and paste in what you copied under a section called `patch`, and add `schema: lumen_pinyin` to the `schema_list`, like so: 
    ```
    patch:
      schema_list: 
        - schema: luna_pinyin
        # possible additional schema entries here
        - schema: lumen_pinyin
    ```
    This will override the default list of input methods. ([Chinese instructions](https://github.com/rime/home/wiki/CustomizationGuide#%E4%B8%80%E4%BE%8B%E5%AE%9A%E8%A3%BD%E6%96%B9%E6%A1%88%E9%81%B8%E5%96%AE))
4. Rebuild Rime by selecting 重新佈署 under the Rime settings, located where your input method menu is. ([Chinese instructions](https://github.com/rime/home/wiki/CustomizationGuide#%E9%87%8D%E6%96%B0%E4%BD%88%E7%BD%B2%E7%9A%84%E6%93%8D%E4%BD%9C%E6%96%B9%E6%B3%95))

Usage
---
After installing, make sure you have Rime enabled, then place your cursor in a text area and use `F4` or `Ctrl` + `` ` `` to bring up Rime's input method selection menu. Select `Pīnyīn` for Lumen Pinyin.

Lumen Pinyin works like a pinyin-based character input system: type words or initials in pinyin, then choose from the selection menu that pops up. 

* The space bar selects the top word (or the selected word, if you've navigated down). 
* Arrow keys navigate the menu.
* Number keys select the corresponding word from the menu.
* `Enter` ignores the selection menu and inputs whatever you've typed directly. 

For more detailed instructions, see the [Rime user guide](https://github.com/rime/home/wiki/UserGuide) (in Chinese). 

Flaws
---
This input method has some flaws, which include the following:

* There is no way to type and select full phrases at a time, because words are joined without spaces between them. You will have to type one word at a time.
* The dictionary contains many entries that are not used in the modern language or not rendered with the proper spaces or capitalization. You will have to ignore these.
* All four-syllable words and phrases are given in two forms: one without any spaces or hyphenation, and one with a hyphen separating the first two and last two syllables. You will have to select the correct one based on the word.

These flaws exist because Rime is optimized for inputting Chinese characters instead of pinyin orthography, as were the dictionary files from which the Lumen Pinyin files were generated. 

Even with its shortcomings, Lumen Pinyin should still be easier to use than entering tone-marked characters individually. 

Source files
---
This repository also contains a `gen` folder which contains the files used to generate the dictionary file `lumen_pinyin.dict.yaml`. These are included only for reference. The files are:

* `generate_dict.py`: a Python script used to generate the dictionary file
* `essay.txt`: a lexicon of Chinese words and phrases with their frequencies, taken from the [Baguwen](https://github.com/rime/rime-essay) (八股文) repository
* `terra_pinyin.dict.yaml`: a dictionary file that lists the pronunciation of words and characters, taken from the [Terra Pinyin](https://github.com/rime/rime-terra-pinyin) (地球拼音) repository

Resources
---

### Rime documentation ###

To learn how to use Rime, customize Rime, or edit schema files, please see the Rime documentation. In particular, I found the following resources helpful (all in Chinese): 
* [User Guide](https://github.com/rime/home/wiki/UserGuide) (說明書), which gives instructions on how to use Rime 
* [Customization Guide](https://github.com/rime/home/wiki/CustomizationGuide) (定製指南), which gives instructions for customizing Rime
* [Rime with Schemata](https://github.com/rime/home/wiki/RimeWithSchemata) (輸入方案設計書), which gives instructions for creating your own input method schema
* [Schema.yaml 詳解](https://github.com/LEOYoon-Tsaw/Rime_collections/blob/master/Rime_description.md), which gives a detailed description of each field in `schema.yaml` and `dict.yaml` files

### Pinyin resources ###

On the benefits of reading and writing in pinyin, see the following blog posts by Victor Mair: 

* [How to learn to read Chinese](https://languagelog.ldc.upenn.edu/nll/?p=189) (May 2008)
* [The future of Chinese language learning is now](https://languagelog.ldc.upenn.edu/nll/?p=11580) (April 2014)
* [How to learn to read and write Chinese](https://languagelog.ldc.upenn.edu/nll/?p=43981) (August 2019) 

I have also written a brief post on learning Chinese that reiterates many of his points: 

* [An Approach to Learning Chinese](https://williampan.net/notes/learning-chinese/) (June 2020) 

For the rules of pinyin orthography, see: 

* [Basic Rules of Hanyu Pinyin Orthography (Summary)](http://pinyin.info/readings/zyg/rules.html) (2003)

For a list of texts written in pinyin orthography, see: 

* [Online texts in Hanyu Pinyin](http://pinyin.info/news/2008/online-texts-in-hanyu-pinyin/) (May 2008)