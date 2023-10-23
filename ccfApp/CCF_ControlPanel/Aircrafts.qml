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
    id: servicesPage
    
    anchors.fill: parent
    anchors.topMargin: 3
    anchors.leftMargin: 5
    anchors.bottomMargin: 5
    anchors.rightMargin: 5

    Menu {
        id: menu
        menuHeight: 45
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 5

        onButtonJsonClick: {
            ACPanel.stop_ccf()
            ACPanel.read_json_file()
            ACPanel.ac_info_init()
            ACPanel.delta_info_init()
        }

        onButtonLaunchClick: {
            ACPanel.try_launch_ccf()
        }
    }

    ACView {
        id: acView

        anchors.left: parent.left
        anchors.right: deltaView.left
        anchors.top: menu.bottom
        anchors.bottom: logView.top
        anchors.rightMargin: 15
        anchors.topMargin: 5
        anchors.bottomMargin: 5
    }

    LogView {
        id: logView

        anchors.left: parent.left
        anchors.right: deltaView.left
        anchors.bottom: parent.bottom
        anchors.rightMargin: 15

        height: 200
    }

    DeltaView {
        id: deltaView

        width: 300
        anchors.right: parent.right
        anchors.top: menu.bottom
        anchors.bottom: parent.bottom
        anchors.rightMargin: 5
        anchors.topMargin: 5
    }
}