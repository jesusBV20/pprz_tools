// Copyright (C) 2023 Jesús Bautista Villar <jesbauti20@gmail.com>
//
// This file is part of paparazzi.
//
// paparazzi is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2, or (at your option)
// any later version.
//
// paparazzi is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with paparazzi; see the file COPYING.  If not, see
// <http://www.gnu.org/licenses/>.

import QtQuick
import QtQuick.Layouts 
import QtQuick.Controls

Item {
    id: menu

    signal buttonJsonClick
    signal buttonLaunchClick

    property real menuWidth: 400
    property real menuHeight: 50

    height: menuHeight
    width: menuWidth
    
    ColumnLayout {
        id: layoutJson
        
        Text {
            text: "JSON config file (should be in the 'formation' folder):"
        }
        
        RowLayout {
            TextField {
                id: jsonText
                Layout.preferredWidth: 355

                text: ACPanel.json_file
                placeholderText: qsTr(".json file name")
                onEditingFinished: {
                    ACPanel.json_file = text
                }
            }

            ButtonAnim {
                id: jsonButton
                buttonText: "Load"
                
                buttonColor: "#525252"
                buttonWidth: 60
                buttonHeight: menuHeight * 0.55
                
                onButtonClick: {
                    menu.buttonJsonClick()
                }
            }
        }
    }

    ButtonAnim {
        id: launchButton

        anchors.top: parent.top
        anchors.right: parent.right

        buttonWidth: 200
        buttonHeight: menuHeight

        buttonText: (ACPanel.ccfstate) ? "Stop CCF" : "Launch CCF"
        buttonTextColor: (ACPanel.ccfstate) ? "green" : "red"

        onButtonClick: {
            menu.buttonLaunchClick()
            buttonText: (ACPanel.ccfstate) ? "Stop CCF" : "Launch CCF"
            buttonTextColor: (ACPanel.ccfstate) ? "green" : "red"
        }
    }
}