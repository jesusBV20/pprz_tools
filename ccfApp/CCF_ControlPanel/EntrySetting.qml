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
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    property string paramText: "param"
    property real textWidth: 60
    property bool textBold: false
    property real maxDigits: 5
    
    property int decimals: 2
    property real from: 0
    property real value: 1
    property real to: 100
    property real step: Math.pow(10, -decimals)
    
    id: layout
    spacing: 4

    signal settingUpdate
    
    Text {
        id: spinText
        text: layout.paramText
        font.bold: layout.textBold
        Layout.preferredWidth: textWidth
    }

    SpinBox {
        readonly property int decimalFactor: Math.pow(10, layout.decimals)
        readonly property real fromSpin: layout.from * decimalFactor
        readonly property real toSpin: layout.to * decimalFactor
        readonly property real stepSpin: layout.step * decimalFactor
        readonly property real initValue: layout.value * decimalFactor

        id: spinBox
        Layout.preferredWidth: 25 + 9*maxDigits

        from: fromSpin
        value: initValue
        to: toSpin
        stepSize: stepSpin
        editable: true

        function decimalToInt(decimal) {
            return decimal * decimalFactor
        }

        validator: DoubleValidator {
            bottom: Math.min(spinBox.from, spinBox.to)
            top:  Math.max(spinBox.from, spinBox.to)
            decimals: layout.decimals
            notation: DoubleValidator.StandardNotation
        }

        textFromValue: function(value, locale) {
            return Number(value / decimalFactor).toLocaleString(locale, 'f', layout.decimals)
        }

        valueFromText: function(text, locale) {
            return Math.round(Number.fromLocaleString(locale, text) * decimalFactor)
        }

        onValueModified: {
            layout.value = spinBox.value / decimalFactor
            layout.settingUpdate()
        }
    }
}