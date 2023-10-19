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

Rectangle {
        id: box_aicrafts
        
        border.width: 1
        border.color: "black"
        color: "lightgray"

        ListView {
            id: list
            anchors.fill: parent
            anchors.topMargin: 6
            anchors.leftMargin: 6
            anchors.bottomMargin: 6
            anchors.rightMargin: 6
            spacing: 3
            clip: true

            model: ACPanel.ac_info_list
            
            delegate: Rectangle {
                required property var modelData
                
                id: box
                width: list.width
                height: 60
                color: "gray"
                border.width: 1
                border.color: "black"
                

                MouseArea {
                    anchors.fill: parent
                }
                
                ColumnLayout {
                    id: idText
                    width: 40
                    anchors.left: box.left
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    spacing:0

                    Text {
                        text: "AC"
                        font.pointSize: 18
                        color: "black"
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBotton
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideMiddle
                        wrapMode: Text.Wrap
                    }

                    Text {
                        text: box.modelData.idLabel
                        
                        font.pointSize: 16
                        color: "black"
                        font.bold: true
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideMiddle
                        wrapMode: Text.Wrap
                    }
                }

                ColumnLayout {
                    id: statusText
                    width: 50
                    anchors.left: idText.right
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    anchors.topMargin: 5
                    anchors.bottomMargin: 5
                    spacing:0

                    Rectangle {
                        width: 40
                        height: 20
                        color: "lightgray"
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Text {
                            anchors.fill: parent
                            text: "NAV"
                            color: (box.modelData.nav_state) ? "darkgreen" : "darkred"
                            font.pointSize: 10
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }

                    Rectangle {
                        width: 40
                        height: 20
                        color: "lightgray"
                        Layout.alignment: Qt.AlignHCenter
                        Text {
                            anchors.fill: parent
                            text: "GVF"
                            color: (box.modelData.gvf_state) ? "darkgreen" : "darkred"
                            font.pointSize: 10
                            font.bold: true
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
                
                
                Rectangle {
                    width: 2
                    anchors.left: statusText.right
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    anchors.topMargin: 4
                    anchors.bottomMargin: 4

                    color: "black"
                }

                ColumnLayout {
                    id: ac_layout
                    anchors.left: statusText.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 4
                    anchors.leftMargin: 12
                    anchors.bottomMargin: 4
                    anchors.rightMargin: 6

                    RowLayout {
                        spacing: 10

                        EntryInfo {
                            id: ell_aInfo

                            infoText: "ell_a"
                            infoValue: box.modelData.ell_a
                            maxDigits: 5
                            buttonTextColor: (ACPanel.ccfstate) ? "darkgreen" : "black"
                        }

                        EntryInfo {
                            id: ell_bInfo

                            infoText: "ell_b"
                            infoValue: box.modelData.ell_b
                            maxDigits: 5
                            buttonTextColor: (ACPanel.ccfstate) ? "darkgreen" : "black"
                        }
                    }
                    
                    RowLayout {
                        EntrySetting {
                            id: keSetting
                            paramText: "ke"
                            textWidth: 20

                            decimals: 1
                            from: 0
                            to: 20
                            value: box.modelData.ke
                 
                            onSettingUpdate: {
                                box.modelData.ke = keSetting.value
                            }
                        }

                        EntrySetting {
                            id: knSetting
                            paramText: "kn"
                            textWidth: 20

                            decimals: 1
                            from: 0
                            to: 20
                            value: box.modelData.kn
                 
                            onSettingUpdate: {
                                box.modelData.kn = knSetting.value
                            }
                        }
                    }

                }

                ButtonAnim {
                    id: chechButton

                    anchors.right: rightSept.left
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    anchors.rightMargin: 8
                    anchors.topMargin: 15
                    anchors.bottomMargin: 15

                    buttonWidth: chechButton.height

                    buttonText: (box.modelData.info_checked) ? "\u2611": "\u2610"
                    buttonColor: (box.modelData.info_checked) ? "darkgreen": "darkred"
                    buttonTextColor: "black"
                    buttonTextSize: 34
                    borderWidht: 10
                    borderColor: "black"

                    onButtonClick: {
                        box.modelData.change_info_checked()
                    }
                }

                Rectangle {
                    id: rightSept
                    width: 2
                    anchors.right: acmenu_layout.left
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    anchors.rightMargin: 6
                    anchors.topMargin: 4
                    anchors.bottomMargin: 4

                    color: "black"
                }
                
                ColumnLayout {
                    id: acmenu_layout

                    anchors.right: parent.right
                    anchors.top: box.top
                    anchors.bottom: box.bottom
                    anchors.rightMargin: 6
                    anchors.topMargin: 4
                    anchors.bottomMargin: 4

                    ButtonAnim {
                        id: update_button

                        buttonWidth: 60
                        buttonHeight: 20

                        buttonText: (box.modelData.status) ? "update" : "..."
                        buttonColor: "lightgray"
                        buttonTextColor: "black"
                        borderWidht: 10
                        borderColor: "black"

                        onButtonClick: {
                            ACPanel.get_ac_dl_values(box.modelData.id)
                            keSetting.value = box.modelData.ke
                            knSetting.value = box.modelData.kn
                        }
                    }

                    ButtonAnim {
                        id: commit_button

                        buttonWidth: 60
                        buttonHeight: 20

                        buttonText: "commit"
                        buttonColor: "lightgray"
                        buttonTextColor: "black"
                        borderWidht: 10
                        borderColor: "black"

                        onButtonClick: {
                            ACPanel.commit_settings(box.modelData.id)
                        }
                    }
                }

                

            }
        }
    }