# cifiro
Library Secruity dependency Checker

Uses api.firosolutions.com to check a Rust or a NodeJS repo for library security holes 

## Support languages:
*  Rust
*  NodeJS


```shell
git clone https://github.com/GhostPirateGir/mkpw.git
$ cd mkpw/ && wget https://raw.githubusercontent.com/firosolutions/cifiro/master/cifiro.py
$  python3.6 cifiro.py
checking key                                                                    
checked key!                                                                    
detected Rust                                                                   
i found the Cargo.toml!                                                         
Checking library pancurses version 0.12                                         
Result:                                                                         
{                                                                               
    "author": "Rust Project Developers",                                        
    "cve": "RUSTSEC-2019-0005",                                                 
    "description": "Description pancurses::mvprintw and pancurses::printw passes
 a pointer from a rust &amp;amp;str to C, allowing hostile input to execute a fo
rmat string attack, which trivially allows writing arbitrary data to stack memor
y. More Info https://github.com/RustSec/advisory-db/issues/106 Patched Versions"
,                                                                               
    "link": "https://rustsec.org/advisories/RUSTSEC-2019-0005.html",            
    "published_date": "2019-06-15T01:00:00",                                    
    "recommendation": "Update to the latest Rust library version",              
    "title": "RUSTSEC-2019-0005: pancurses: Format string vulnerabilities in `pa
ncurses`",                                                                      
    "version": "not set"                                                        
}                                                                               
Checking library rand version 0.3                                               
Result:                                                                         
 nothing found                                                                  
Checking library md-5 version 0.5                                               
Result:                                                                         
 nothing found                                                                  
Checking library base64 version 0.8                                             
Result:                                                                         
 nothing found                                                                  
```


### Apikey as a system argument supported
```
$ wget https://raw.githubusercontent.com/firosolutions/cifiro/master/cifiro.py
$ python3.6 cifiro.py apikey=myapigoeshere
```
