Script to check for incorrect property declarations, for example strong IBOutlets

````
./VoiceView.m:28:@property (strong, nonatomic) IBOutlet UIView *mailContainer; should probably be weak
````
In strict mode, it will also warn you if you did not explictly set "assign" for primitives and "strong" for pointers.

````
./VoiceView.m:46:@property(nonatomic) BOOL volumeTooLow; should probably be assign
````

To install
````
git clone git@github.com:reigndesign/propcheck.git
cp propcheck.py /usr/local/bin/propcheck
````

To use in current folder with default options
````
propcheck
````

To use in custom folder
````
propcheck --path path/to/Classes
````

To use in strict mode (warns if you dont use explicit strong and assign)
````
propcheck --strict 
````
