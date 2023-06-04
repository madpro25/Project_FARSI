#!/usr/bin/bash

home_dir=$(pwd)
cacti_dir=cacti_for_FARSI
cacti_dir_full=$home_dir\/cacti_for_FARSI
# Check for cacti_for_FARSI directory
cacti=cacti_for_FARSI/cacti
if test -f "$cacti"; then
    # Setting up home_settings.py
    case `grep -x "home_dir = \"$home_dir\"" "data_collection/collection_utils/home_settings.py" > /dev/null; echo $?` in
        0)
        echo home_settings already configured
        ;;
        1)
        echo home_dir = \"$home_dir\" >> data_collection/collection_utils/home_settings.py
        echo sys.path.append\(home_dir\) >> data_collection/collection_utils/home_settings.py
        echo Configured home_settings.py
        ;;
        *)
        ;;
    esac

    # Setting up config_cacti.py
    case `grep -x "cacti_bin_addr = \"$cacti_dir_full/cacti\"" "settings/config_cacti.py" > /dev/null; echo $?` in
        0)
        echo config_cacti already configured
        ;;
        1)
        echo cacti_bin_addr = \"$cacti_dir_full\/cacti\" >> settings/config_cacti.py
        echo cacti_param_addr = \"$cacti_dir_full\/farsi_gen.cfg\" >> settings/config_cacti.py
        echo cacti_data_log_file = \"$cacti_dir_full\/data_log.csv\" >> settings/config_cacti.py
        echo Configured config_cacti.py
        ;;
        *)
        ;;
    esac
    # Adding cacti folder to .gitignore
    if grep -xq "$cacti_dir" ".gitignore"; then
        echo cacti already added to .gitignore
    else 
        echo $cacti_dir >> .gitignore
        echo Added cacti_for_FARSI to .gitignore
    fi
else 
    echo cacti executable not found
    echo Please build cacti_for_FARSI before continuing with the environment setup
fi 