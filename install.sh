#!/usr/bin/env bash


install_dir="/usr/local/bin"
required_lib="python3-venv"

read -p "[default n] type y/n to proceed : " inpt
if [[ $inpt == "y" ]];
    then 
        check="$(apt list | grep -q $required_lib)"
        echo "$check" # if return something then do
        if $check
            then
                # create the virtual environment
                python3 -m venv venv
                # activate it
                source venv/bin/activate
                # insure pip is upgraded to the latest version inside the environment 
                pip install --upgrade pip
                # installing the component of the editor
                pip install -r requirements.txt
                # make the file exceutable
                chmod +x Spectrum.py
                # create a symlink
                ln -s $(pwd)/Spectrum.py $HOME/.local/bin/runspectrum
                echo "#!/usr/bin/env bash
dir=$(pwd)
source \$dir/venv/bin/activate 
runspectrum" > spectrum
                chmod +x spectrum
                mv spectrum $HOME/.local/bin/
                
                echo "installation done successfully"
                echo "لقد تمت عملية التنزيل بنجاح "
                echo "you can now run spectrum Ide by running the command 'spectrum'"
                # run the program
                sleep 4s
                spectrum

        else
            echo "if any errors happens please run the below command"
            echo "اذا حدث خطأ اثناء عملية التنزيل الرجاء تنفيذ السطر التالي"
            echo "sudo apt install $required_lib"
        fi
elif [[ $inpt == "n" ]]
    then
        echo "installation canceled"
else
    echo "y or n has to be entered in order to continue"
fi
