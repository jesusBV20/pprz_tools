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
    Text {
        id: colsole_text
        anchors.top: parent.top
        height:20

        font.pointSize: 12
        font.bold: true
        text: "Log console:"
        color: "black"
    }

    Rectangle {
        id: box_logview
        anchors.top: colsole_text.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        border.width: 1
        border.color: "black"
        color: "#adadad"

        

        ScrollView {
            id: scrollText
            anchors.fill: parent
            anchors.leftMargin: 5
            anchors.topMargin: 5
            anchors.bottomMargin: 5

            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
            ScrollBar.vertical.position: consoleText.contentHeight

            contentHeight: consoleText.contentHeight
            //ScrollBar.vertical.position: box_logview.scrollPosition

            TextEdit {
                id: consoleText
                width: scrollText.width - 10

                font.pointSize: 10
                text: ACPanel.reporter.console_log
                color: "black"
                wrapMode: Text.Wrap
                readOnly: true
                selectByMouse: true
            } 
        }
    }
}
