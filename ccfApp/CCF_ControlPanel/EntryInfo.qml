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
    property string infoText: "param"
    property string buttonTextColor: "black"
    property string infoValue: "-"
    property real maxDigits: 5

    id: layout
    spacing: 4
    
    Text {
        id: spinText
        text: infoText
    }

    ButtonAnim {
        buttonText: infoValue
        buttonColor: "lightgray"
        buttonTextColor: layout.buttonTextColor
        borderWidht: 10
        borderColor: "black"

        buttonWidth: 6 + 9*maxDigits
        buttonHeight: 20
    }
}