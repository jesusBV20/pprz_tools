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

RowLayout {
    id: layout

    property real buttonWidth: 40
    property real buttonHeight: 20
    property string buttonText: "button"
    property string buttonColor: "#363636"
    property string buttonTextColor: "#E3E3E3"
    property real buttonTextSize: 0
    property real borderWidht: 1
    property string borderColor: buttonColor

    width: buttonWidth
    height: buttonHeight

    signal buttonClick

    Rectangle {
        id: button

        width: layout.width
        height: layout.height
        color: buttonColor
        
        border.width: borderWidht
        border.color: buttonColor
        radius: 0

        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        Text {
            id: text
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
            text: buttonText
            color: buttonTextColor
            font.pointSize: (buttonTextSize > 0) ? buttonTextSize : button.height * 0.55 + 1
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }

        MouseArea {
            anchors.fill: parent
            onPressed: {
                text.font.bold = true
                text.font.pointSize = (buttonTextSize > 0) ? text.font.pointSize*0.95 : text.font.pointSize * 0.8
            }

            onReleased: {
                text.font.bold = false
                text.font.pointSize = (buttonTextSize > 0) ? buttonTextSize : button.height * 0.55 + 1
            }

            onClicked: {
                layout.buttonClick()
            }
        }
    }
}