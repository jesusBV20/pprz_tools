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

Item {
    Rectangle {
        id: box_deltas
        
        anchors.top: parent.top
        width: parent.width
        height: parent.height - 50

        border.width: 1
        border.color: "black"
        color: "lightgray"

        RowLayout {
            id: ccfsetttingLayout
            height: 40
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 10

            EntrySetting {
                id: kSetting

                paramText: "k_ccf"
                textWidth: 50

                decimals: 1
                from: 0
                to: 100
                value: ACPanel.k_ccf    

                onSettingUpdate: {
                    ACPanel.k_ccf = kSetting.value
                }
            }

            EntrySetting {
                id: uSetting

                paramText: "u_max"
                textWidth: 50
                maxDigits: 6

                decimals: 1
                from: 0
                to: 1000
                step: 1
                value: ACPanel.u_max   

                onSettingUpdate: {
                    ACPanel.u_max = uSetting.value
                }
            }
        }
        

        Rectangle {
            id: sep
            height: 2
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: ccfsetttingLayout.bottom
            anchors.topMargin: 6
            anchors.leftMargin: 12
            anchors.bottomMargin: 6
            anchors.rightMargin: 12
            

            color: "black"
        }

        ListView {
            id: list
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: sep.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 6
            anchors.leftMargin: 6
            anchors.bottomMargin: 6
            anchors.rightMargin: 6
            spacing: 3
            clip: true

            model: ACPanel.delta_info_list
            
            delegate: Rectangle {
                required property var modelData
                
                id: box
                width: list.width
                height: 30
                color: "gray"
                border.width: 1
                border.color: "black"
                

                MouseArea {
                    anchors.fill: parent
                }
                
                Text {
                    id: deltaText
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 5

                    text: "\u03B4"
                    font.pointSize: 12
                    color: (box.modelData.buffered_flag) ? "darkred" : "black"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                EntrySetting {
                    id: deltaSetting
                    anchors.left: deltaText.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 10

                    paramText: box.modelData.id_from + " \u2794 " + box.modelData.id_to
                    textWidth: 80
                    textBold: true

                    decimals: 0
                    from: 0
                    to: 360
                    value: box.modelData.value  

                    onSettingUpdate: {
                        box.modelData.value_buffer = deltaSetting.value
                        box.modelData.buffered_flag = true
                    }
                }

                EntryInfo {
                    id: errorInfo
                    anchors.left: deltaSetting.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 10

                    infoText: "error"
                    infoValue: box.modelData.error
                    maxDigits: 5
                    buttonTextColor: "black"
                }
            }
        }
    }

    ButtonAnim {
        id: commit_button

        anchors.top: box_deltas.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 5

        buttonWidth: parent.width

        buttonText: "Commit \u03B4s"
        buttonTextColor: "white"
        borderWidht: 1
        borderColor: "black"

        onButtonClick: {
            ACPanel.commit_all_delta()
        }
    }
}
