/****************************************************************************
** Generated QML type registration code
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <QtQml/qqml.h>
#include <QtQml/qqmlmoduleregistration.h>

#if __has_include(<C:/Users/HP/Documents/sans_titre2/api/GridParametersQML.py>)
#  include <C:/Users/HP/Documents/sans_titre2/api/GridParametersQML.py>
#endif


#if !defined(QT_STATIC)
#define Q_QMLTYPE_EXPORT Q_DECL_EXPORT
#else
#define Q_QMLTYPE_EXPORT
#endif
Q_QMLTYPE_EXPORT void qml_register_types_io_qml()
{
    QT_WARNING_PUSH QT_WARNING_DISABLE_DEPRECATED
    qmlRegisterTypesAndRevisions<GridParametersQML>("io.qml", 1);
    QT_WARNING_POP
    qmlRegisterModule("io.qml", 1, 0);
}

static const QQmlModuleRegistration ioqmlRegistration("io.qml", qml_register_types_io_qml);
