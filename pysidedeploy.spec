[app]

# title of your application
title = NWIM

# project directory. the general assumption is that project_dir is the parent directory
# of input_file
project_dir = C:\Users\HP\Documents\sans_titre2

# source file path
input_file = C:\Users\HP\Documents\sans_titre2\main.py

# directory where the executable output is generated
exec_directory = C:\Users\HP\Documents\sans_titre2

# path to .pyproject project file
project_file = sans_titre2.pyproject

# application icon
icon = C:\Users\HP\Downloads\nwim.ico

[python]

# python path
python_path = C:\Users\HP\AppData\Local\Programs\Python\Python311\python.exe

# python packages to install
packages = Nuitka==2.5.1

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# comma separated path to qml files required
# normally all the qml files required by the project are added automatically
qml_files = frontend\components\chartsComponents\QobsChart.qml,frontend\components\chartsComponents\ETPChart.qml,frontend\components\pages\GridParametersDialog.qml,frontend\components\chartsComponents\RainChart.qml,frontend\components\chartsComponents\TempChart.qml,frontend\components\parameters\GridParameters.qml,frontend\components\parameters\Parameters.qml,frontend\components\parameters\RangeParameters.qml,main.qml,frontend\components\datasetComponents\LoadDataComponent.qml,frontend\components\datasetComponents\QobsComponent.qml,frontend\components\datasetComponents\StatisticsComponent.qml,frontend\components\datasetComponents\ETPComponent.qml,frontend\components\datasetComponents\TempComponent.qml,frontend\components\datasetComponents\RainComponent.qml,frontend\components\chartsComponents\SimChart.qml,frontend\components\customComponents\CustomCheckDelegate.qml,frontend\components\customComponents\CalendarDialog.qml,frontend\components\customComponents\DataErrorsDialog.qml,frontend\components\customComponents\CustomComboBox.qml,frontend\components\customComponents\CustomToolButton.qml,frontend\components\customComponents\CustomFolderDialog.qml,frontend\components\pages\ETPComputing.qml,frontend\components\pages\Regression.qml,frontend\components\customComponents\CustomTabBarButton.qml,frontend\components\customComponents\CustomRadioButton.qml,frontend\components\customComponents\CustomTextField.qml,frontend\components\customComponents\CustomSlider.qml,frontend\components\pages\BaseFlow.qml

# excluded qml plugin binaries
excluded_qml_plugins = QtSensors,QtWebEngine

# qt modules used. comma separated
modules = Network,Quick,Qml,QmlModels,OpenGL,Gui,Core,QmlWorkerScript,Widgets,QuickControls2,QmlMeta,QuickTemplates2

# qt plugins used by the application. only relevant for desktop deployment. for qt plugins used
# in android application see [android][plugins]
plugins = scenegraph,styles,qmltooling

[android]

# path to pyside wheel
wheel_pyside = 

# path to shiboken wheel
wheel_shiboken = 

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = 

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default is onefile.
mode = onefile

# (str) specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations --include-module=sklearn.tree._partitioner --no-debug-immortal-assumptions

[buildozer]

# build mode
# possible options = [release, debug]
# release creates an aab, while debug creates an apk
mode = debug

# contrains path to pyside6 and shiboken6 recipe dir
recipe_dir = 

# path to extra qt android jars to be loaded by the application
jars_dir = 

# if empty uses default ndk path downloaded by buildozer
ndk_path = 

# if empty uses default sdk path downloaded by buildozer
sdk_path = 

# other libraries to be loaded. comma separated.
# loaded at app startup
local_libs = 

# architecture of deployed platform
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
arch = 

