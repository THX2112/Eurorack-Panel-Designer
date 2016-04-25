#!/usr/bin/env python
# 
# Eurorack Panel Designer by THX2112
#
# v4
# - reference: http://www.doepfer.de/a100_man/a100m_e.htm
# Adds lasercutting color and refactoring

import sys
import math

import inkex
from simplestyle import *

Orange = '#f6921e'
Blue =   '#0000FF'
White =  '#FFFFFF'
lasercut_width = '0.01mm'
Panel_color = '#e6e6e6'


class EurorackPanelEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-t', '--hp', action='store', type='int', dest='hp', default=6, help='Panel HP?')
        self.OptionParser.add_option('-o', '--offset', action='store', type='float', dest='offset', default=0.36, help='Amount of material to remove for fitting?')
        self.OptionParser.add_option('-s', '--symmetrical', action='store', type='inkbool', dest='symmetrical', default='False', help='Remove material from both sides?')
        self.OptionParser.add_option('-v', '--oval', action='store', type='inkbool', dest='oval', default='False', help='Oval holes?')
        self.OptionParser.add_option('-c', '--centers', action='store', type='inkbool', dest='centers', default='False', help='Mark centers?')
        self.OptionParser.add_option('-l', '--lasercut', action='store', type='inkbool', dest='lasercut', default='False', help='Lasercut style?')

    def draw_SVG_Panel(self, (w,h), (x,y), (rx,ry), parent):
        " Draw the Basic Panel Shape"
        if self.options.lasercut:
            stroke = Blue
            width = lasercut_width
            fill = 'none'
        else:
            stroke = 'none'
            width =  '0mm'
            fill =   Panel_color
        #
        style = { 'stroke'        : stroke,  # 'none',
                  'stroke-width'  : width,   # '0mm',
                  'fill'          : fill     # '#e6e6e6'
                }
        attr  = { 'style'   : formatStyle(style),
                  'height'  : str(h),
                  'width'   : str(w),
                  'x'       : str(x),
                  'y'       : str(y),
                  'rx'      : str(rx),
                  'ry'      : str(ry)
                }
        circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attr)

    def draw_SVG_square(self, (w,h), (x,y), (rx,ry), parent):
        " Draw Oval shaped holes "
        if self.options.lasercut:
            stroke = Blue
            width = lasercut_width
            fill = 'none'
        else:
            stroke = 'none'
            width =  '0mm'
            fill =   White
        style = { 'stroke'        : stroke,   # 'none',
                  'stroke-width'  : width,   # '0mm',
                  'fill'          : fill     # '#ffffff'
                }
        attr =  { 'style'   : formatStyle(style),
                  'height'  : str(h),
                  'width'   : str(w),
                  'x'       : str(x),
                  'y'       : str(y),
                  'rx'      : str(rx),
                  'ry'      : str(ry)
                }
        circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attr)
    
    def draw_SVG_ellipse(self, (rx, ry), (cx, cy), parent, start, end):
        " Draw Round holes "
        if self.options.lasercut:
            stroke = Blue
            width = lasercut_width
            fill = 'none'
        else:
            stroke = 'none'
            width =  '0mm'
            fill =   White
        style = { 'stroke'        : stroke,   # 'none',
                  'stroke-width'  : width,   # '0mm',
                  'fill'          : fill     # '#ffffff'            
                }
        ell_attr = {'style' : formatStyle(style),
                    inkex.addNS('cx','sodipodi')      :str(cx),
                    inkex.addNS('cy','sodipodi')      :str(cy),
                    inkex.addNS('rx','sodipodi')      :str(rx),
                    inkex.addNS('ry','sodipodi')      :str(ry),
                    inkex.addNS('start','sodipodi')   :str(start),
                    inkex.addNS('end','sodipodi')     :str(end),
                    inkex.addNS('open','sodipodi')    :'true',    #all ellipse sectors we will draw are open
                    inkex.addNS('type','sodipodi')    :'arc'
                   }
        ell = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), ell_attr)

    def draw_SVG_line(self,  (x1, y1), (x2, y2), parent):
        " draw an SVG line segment between the given (raw) points "
        line_style = { 'stroke'       : Orange,   # '#000000',
                       'stroke-width' : '.05mm',
                       'fill'         : 'none'
                     }

        line_attr =  { 'style'        : formatStyle(line_style),
                       'd'            : 'M %s,%s L %s,%s' % (x1,y1, x2,y2)
                     }
        line = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attr)


    def effect(self):

        hp = self.options.hp
        symmetrical = self.options.symmetrical
        offset = self.options.offset
        oval = self.options.oval
        centers = self.options.centers
        unitfactor = self.unittouu('1mm') # all our dimensions are in mm

        # Dimensions
        height = 128.5
        if symmetrical: 
            width = 7.5 + ((hp - 3) * 5.08) + 7.5
        else:
            width = (hp * 5.08) - offset
        
        # Calculate final width and height of panel
        pheight = height * unitfactor
        pwidth =  width * unitfactor
        
        # Build top level group to put everything in
        # Put in in the centre of current view
        group_transform = 'translate(%s,%s)' % (self.view_center[0]-pwidth/2, self.view_center[1]-pheight/2 )
        group_name = 'EuroPanel'
        group_attribs = {inkex.addNS('label','inkscape'):group_name, 'transform':group_transform }
        group = inkex.etree.SubElement(self.current_layer, 'g', group_attribs)

        # Draw Panel
        self.draw_SVG_Panel((pwidth,pheight), (0,0), (0,0), group)

        # Draw Holes
        TopHoles = 3.0
        BottomHoles = 125.5
        LeftHoles = 7.5
        RightHoles = ((hp - 3.0) * 5.08) + 7.5
        HoleRadius = 1.6
        #
        leftH = LeftHoles * unitfactor
        rightH = RightHoles * unitfactor
        bottomH = BottomHoles * unitfactor
        topH = TopHoles * unitfactor
        holeR = HoleRadius * unitfactor
        gap = holeR/2
        #        
        if oval == False:  # Draw Round holes
            rx = HoleRadius * unitfactor
            ry = rx # circles
            end = 2 * 3.14159  # full cirlce.

            # Bottom Left
            self.draw_SVG_ellipse((rx, ry), (leftH, bottomH), group, 0, end)
            # Top Left
            self.draw_SVG_ellipse((rx, ry), (leftH, topH), group, 0, end)

            # Draw Left-side Centers
            if centers == True:
                # Bottom Left Centers
                # Horizontal Line
                self.draw_SVG_line( (leftH-holeR+gap, bottomH), (leftH+holeR-gap, bottomH), group)
                # Vertical Line
                self.draw_SVG_line( (leftH, bottomH+holeR-gap), (leftH, bottomH-holeR+gap), group)
                # Top Left Centers
                # Horizontal Line
                self.draw_SVG_line( (leftH-holeR+gap, topH), (leftH+holeR-gap, topH), group)
                # Vertical Line
                self.draw_SVG_line( (leftH, topH+holeR-gap), (leftH, topH-holeR+gap), group)
            # Draw the Righthand side Mounting holes
            if hp >= 5:
                # Bottom Right
                self.draw_SVG_ellipse((rx, ry), (rightH, bottomH), group, 0, end)
                # Top Right
                self.draw_SVG_ellipse((rx, ry), (rightH, topH), group, 0, end)
                # Draw Right-side Centers
                if centers == True:
                    # Bottom Right Centers - Horizontal Line
                    self.draw_SVG_line( (rightH-holeR+gap, bottomH), (rightH+holeR-gap, bottomH), group)
                    # Vertical Line
                    self.draw_SVG_line( (rightH, bottomH+holeR-gap), (rightH, bottomH-holeR+gap), group)
                    # Top Right Centers - Horizontal Line
                    self.draw_SVG_line( (rightH-holeR+gap, topH), (rightH+holeR-gap, topH), group)
                    # Vertical Line
                    self.draw_SVG_line( (rightH, topH+holeR-gap), (rightH, topH-holeR+gap), group)

        else: # oval == True
            # Oval Holes: (a square with rounded corners)
            oval_size = 5.5  # 3.2mm hole. Oval is 5.5mm across
            oval_stretch = oval_size/2 # 2.75
            #
            gapH = oval_stretch*unitfactor - gap
            oval_offset = (oval_stretch-HoleRadius)*unitfactor # 1.15
            oval_width = oval_size*unitfactor
            oval_height = HoleRadius*2*unitfactor

            # Bottom Left
            self.draw_SVG_square((oval_width,oval_height), (leftH-oval_stretch*unitfactor,bottomH-holeR), (holeR,0), group)
            # Top Left
            self.draw_SVG_square((oval_width,oval_height), (leftH-oval_stretch*unitfactor,topH-holeR), (holeR,0), group)

            # Draw Left-side Centers
            if centers == True:
                # Bottom Left Centers - Horizontal Line
                self.draw_SVG_line( (leftH-gapH, bottomH), (leftH+gapH, bottomH), group)
                # Vertical Lines
                offset = -oval_offset
                for i in range(3):
                    self.draw_SVG_line( (leftH+offset, bottomH+holeR-gap), (leftH+offset, bottomH-holeR+gap), group)
                    offset += oval_offset
                # Top Left Centers - Horizontal Line
                self.draw_SVG_line( (leftH-gapH, topH), (leftH+gapH, topH), group)
                # Vertical Lines
                offset = -oval_offset
                for i in range(3):
                    self.draw_SVG_line( (leftH+offset, topH+holeR-gap), (leftH+offset, topH-holeR+gap), group)
                    offset += oval_offset
            # Draw the Righthand side Mounting holes
            if hp >= 5:
                # Bottom Right
                self.draw_SVG_square((oval_width,oval_height), (rightH-oval_stretch*unitfactor,bottomH-holeR), (holeR,0), group)
                # Top Right
                self.draw_SVG_square((oval_width,oval_height), (rightH-oval_stretch*unitfactor,topH-holeR), (holeR,0), group)

                # Draw Left-side Centers
                if centers == True:
                    # Bottom Right Centers - Horizontal Line
                    self.draw_SVG_line( (rightH-gapH, bottomH), (rightH+gapH, bottomH), group)
                    # Left Vertical Line
                    # Vertical Lines
                    offset = -oval_offset
                    for i in range(3):
                        self.draw_SVG_line( (rightH+offset, bottomH+holeR-gap), (rightH+offset, bottomH-holeR+gap), group)
                        offset += oval_offset
                    # Top Right Centers
                    # Horizontal Line
                    self.draw_SVG_line( (rightH-gapH, topH), (rightH+gapH, topH), group)
                    # Left Vertical Line
                    offset = -oval_offset
                    for i in range(3):
                        self.draw_SVG_line( (rightH+offset, topH+holeR-gap), (rightH+offset, topH-holeR+gap), group)
                        offset += oval_offset



# Create effect instance and apply it.
effect = EurorackPanelEffect()
effect.affect()