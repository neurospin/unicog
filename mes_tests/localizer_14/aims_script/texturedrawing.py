# -*- coding: utf-8 -*-

#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
import anatomist.direct.api as anatomist
from soma import aims
from soma.aims import colormaphints
import sys, os, math
sys.path.insert( 0, '.' )

userLevel = 4
# determine wheter we are using Qt4 or Qt3, and hack a little bit accordingly
# the boolean qt4 gloabl variable will tell it for later usage
qt4 = True
from PyQt4 import QtCore, QtGui
qt = QtGui
from PyQt4.uic import loadUi

# do we have to run QApplication ?
if qt.qApp.startingUp():
  qapp = qt.QApplication( sys.argv )
  runqt = True
else:
  runqt = False

#import sphere
import numpy

selmesh = None
selanamesh = None

class TexDrawAction( anatomist.cpp.Action ):
  def name( self ):
    return 'TexDrawAction'

  def takePolygon( self, x, y, globx, globy ):
    #print 'takePolygon', x, y
    w = self.view().aWindow()
    obj = w.objectAtCursorPosition( x, y )

    if obj is not None:
      print 'object:', obj, obj.name()
      surf = None
      if obj.objectTypeName( obj.type() ) == 'SURFACE':
        surf = obj
      elif isinstance( obj, anatomist.cpp.MObject ):
        surf = [ o for o in obj if o.type() == 3 ]
        if len( surf ) != 1:
          return
        surf = surf[0]
      if surf is not None:
        poly = w.polygonAtCursorPosition( x, y, obj )
        if poly == 0xffffff: # white
          return # background
        print 'polygon:', poly
        mesh = anatomist.cpp.AObjectConverter.aims( surf )
        #print 'mesh:', mesh
        ppoly = mesh.polygon()[poly]
        vert = mesh.vertex()
        global selmesh, selanamesh
        if selmesh is None:
          selmesh = aims.AimsSurfaceTriangle()
        selmesh.vertex().assign( [ vert[ppoly[0]], vert[ppoly[1]],
          vert[ppoly[2]] ] )
        selmesh.polygon().assign( [ aims.AimsVector_U32_3( 0, 1, 2 ) ] )
        if selanamesh is None:
          selanamesh = anatomist.cpp.AObjectConverter.anatomist( selmesh )
          a = anatomist.Anatomist()
          a.execute( 'SetMaterial', objects=[selanamesh], diffuse=[0,0,1.,1.] )
          a.execute( 'AddObject', objects=[selanamesh], windows=[w] )
        selanamesh.setChanged()
        selanamesh.notifyObservers()

  def delPolygon( self ):
    global selmesh, selanamesh
    selmesh = None
    # keep object ID and release python reference to it
    id = a.convertSingleObjectParamsToIDs( selanamesh )
    selanamesh = None
    a.execute( 'DeleteElement', elements=[ id ] )

  def newtexture( self, x, y, globx, globy ):
    print 'new texture'
    w = self.view().aWindow()
    aw = a.AWindow( a, w )
    obj = w.objectAtCursorPosition( x, y )
    #print 'object:', obj
    if obj is not None:
      if obj.objectTypeName( obj.type() ) == 'SURFACE':
        surf = obj
        texs = []
      #elif obj.objectTypeName( obj.type() ) == 'TEXTURED SURF.':
        #print 'TEXTURED SURF.'
        #surf = [ o for o in obj if o.type() == 3 ]
        #if len( surf ) != 1:
          #print 'not one mesh, but', len( surf )
          #return
        #surf = surf[0]
        #texs = [ o for o in obj if o.type() == 18 ]
        #self._texsurf = obj
        #print 'draw initiated'
        #return
      else:
        return
      gl = surf.glAPI()
      if gl:
        vs = anatomist.cpp.ViewState()
        nv = gl.glNumVertex( vs )
        if nv > 0:
          tex = aims.TimeTexture_FLOAT()
          t = tex[0]
          t.reserve( nv )
          for i in xrange(nv):
            t.push_back(0.)
          atex = a.toAObject( tex )
          #atex = a.AObject( a, surf ).generateTexture()
          texs.append( atex )
          # ...
          tsurf = a.fusionObjects( [ atex, obj ], method='FusionTexSurfMethod' )
          tsurf.setPalette( palette='Blue-Red-fusion' )
          self._texsurf = tsurf
          #tsurf.takeRef()
          aw.removeObjects( obj )
          aw.addObjects( tsurf )

  def startDraw( self, x, y, globx, globy ):
    self._startDraw( x, y, 1. )

  def startErase( self, x, y, globx, globy ):
    self._startDraw( x, y, 0. )

  def _startDraw( self, x, y, value ):
    w = self.view().aWindow()
    obj = w.objectAtCursorPosition( x, y )
    #print 'object:', obj
    if obj is not None:
      texs = []
      if obj.objectTypeName( obj.type() ) == 'SURFACE':
        surf = obj
        p = obj.parents()
        found = False
        for o in p:
          if o.objectTypeName( o.type() ) == 'TEXTURED SURF.' \
            and w.hasObject( o ):
            texs = [ ob for ob in o if ob.type() == 18 ]
            self._texsurf = o
            found = True
            break
        if not found:
          # create a new texture
          self.newtexture( x, y, 0, 0 )
          self._startDraw( x, y, value )
          return
      elif obj.objectTypeName( obj.type() ) == 'TEXTURED SURF.':
        surf = [ o for o in obj if o.type() == 3 ]
        if len( surf ) != 1:
          return
        surf = surf[0]
        texs = [ o for o in obj if o.type() == 18 ]
        self._texsurf = obj
      else:
        return
      if len( texs ) == 0:
        return
      self._surf = surf
      self._tex = texs[-1]
      self._mesh = anatomist.cpp.AObjectConverter.aims( surf )
      self._aimstex = anatomist.cpp.AObjectConverter.aims( self._tex, { 'scale' : 0 } )
      self.draw( x, y, value )

  def endDraw( self, x, y, globx, globy ):
    if hasattr( self, '_aimstex' ):
      del self._aimstex
      del self._mesh
      del self._tex
      del self._surf

  def moveDraw( self, x, y, globx, globy ):
    self.draw( x, y, 1. )

  def erase( self, x, y, globx, globy ):
    self.draw( x, y, 0. )

  def draw( self, x, y, value ):
    if not hasattr( self, '_aimstex' ):
      return
    w = self.view().aWindow()
    obj = self._texsurf
    poly = w.polygonAtCursorPosition( x, y, obj )
    if poly == 0xffffff or poly < 0 or poly >= len( self._mesh.polygon() ):
      return
    ppoly = self._mesh.polygon()[poly]
    print 'poly:', poly, ppoly
    vert = self._mesh.vertex()
    pos = aims.Point3df()
    pos = w.positionFromCursor( x, y )
    print 'pos:', pos
    v = ppoly[ numpy.argmin( [ (vert[p]-pos).norm() for p in ppoly ] ) ]
    print 'vertex:', v, vert[v]
    self._aimstex[0][v] = value
    self._tex.setChanged()
    self._tex.notifyObservers()


class TexDrawControl( anatomist.cpp.Control ):
  def __init__( self, prio = 25 ):
    anatomist.cpp.Control.__init__( self, prio, 'TexDrawControl' )

  def eventAutoSubscription( self, pool ):
    key = QtCore.Qt
    NoModifier = key.NoModifier
    ShiftModifier = key.ShiftModifier
    ControlModifier = key.ControlModifier
    AltModifier = key.AltModifier
    self.mouseLongEventSubscribe( \
      key.LeftButton, NoModifier,
      pool.action( 'TexDrawAction' ).startDraw,
      pool.action( 'TexDrawAction' ).moveDraw,
      pool.action( 'TexDrawAction' ).endDraw,
      False )
    self.mouseLongEventSubscribe( \
      key.LeftButton, NoModifier,
      pool.action( 'TexDrawAction' ).startDraw,
      pool.action( 'TexDrawAction' ).moveDraw,
      pool.action( 'TexDrawAction' ).endDraw,
      False )
    self.mouseLongEventSubscribe( \
      key.LeftButton, ControlModifier,
      pool.action( 'TexDrawAction' ).startErase,
      pool.action( 'TexDrawAction' ).erase,
      pool.action( 'TexDrawAction' ).endDraw,
      False )
    self.mousePressButtonEventSubscribe( \
      key.RightButton, ControlModifier,
      pool.action( 'TexDrawAction' ).newtexture )
    # polygon picking
    self.mousePressButtonEventSubscribe( key.RightButton, NoModifier,
      pool.action( 'TexDrawAction' ).takePolygon )
    self.keyPressEventSubscribe( key.Key_Escape, NoModifier,
      pool.action( "TexDrawAction" ).delPolygon )
    # now plug the standard actions
    self.mouseLongEventSubscribe( key.MidButton, ShiftModifier,
      pool.action( "Zoom3DAction" ).beginZoom,
      pool.action( "Zoom3DAction" ).moveZoom,
      pool.action( "Zoom3DAction" ).endZoom, True )
    self.wheelEventSubscribe( pool.action( "Zoom3DAction" ).zoomWheel )
    self.keyPressEventSubscribe( key.Key_C, ControlModifier,
      pool.action( "Trackball" ).setCenter )
    self.keyPressEventSubscribe( key.Key_C, AltModifier,
      pool.action( "Trackball" ).showRotationCenter )
    self.mouseLongEventSubscribe( key.MidButton, ControlModifier,
      pool.action( "Translate3DAction" ).beginTranslate,
      pool.action( "Translate3DAction" ).moveTranslate,
      pool.action( "Translate3DAction" ).endTranslate, True )
    self.mouseLongEventSubscribe ( \
      key.MidButton, NoModifier,
      pool.action( 'ContinuousTrackball' ).beginTrackball,
      pool.action( 'ContinuousTrackball' ).moveTrackball,
      pool.action( 'ContinuousTrackball' ).endTrackball, True )
    self.keyPressEventSubscribe( key.Key_Space, ControlModifier,
      pool.action( "ContinuousTrackball" ).startOrStop )


#a = anatomist.Anatomist()
#pix = qt.QPixmap( 'control.xpm' )
#anatomist.cpp.IconDictionary.instance().addIcon( 'MyControl',
  #pix )
#ad = anatomist.cpp.ActionDictionary.instance()
#ad.addAction( 'MyAction', lambda: MyAction() )
#cd = anatomist.cpp.ControlDictionary.instance()
#cd.addControl( 'MyControl', lambda: MyControl(), 25 )
#cm = anatomist.cpp.ControlManager.instance()
#cm.addControl( 'QAGLWidget3D', '', 'MyControl' )

#s = sphere.ASphere()
#a.registerObject( s )
#aw = a.createWindow( '3D' )
#a.addObjects( [ s ], [ aw ] )

a = anatomist.Anatomist()

pix = qt.QPixmap( 'control.xpm' )
anatomist.cpp.IconDictionary.instance().addIcon( 'TexDrawControl',
  pix )
ad = anatomist.cpp.ActionDictionary.instance()
ad.addAction( 'TexDrawAction', TexDrawAction )
cd = anatomist.cpp.ControlDictionary.instance()
cd.addControl( 'TexDrawControl', TexDrawControl, 26 )
cm = anatomist.cpp.ControlManager.instance()
cm.addControl( 'QAGLWidget3D', '', 'TexDrawControl' )

s = a.loadObject( 'test.mesh' )
aw = a.createWindow( '3D' )
a.addObjects( [ s ], [ aw ] )
a.execute( 'SetControl', windows=[aw], control='TexDrawControl' )

qt.QMessageBox.information( None, 'texture drawing', '1. put a mesh in a 3D view\n2.select the "Mickey" control\n3. ctrl+right click on the mesh to create an empty texture or initiate the drawinf session\n4. draw on the mesh using the mouse left button\n   ctrl+left button erases', qt.QMessageBox.Ok )

# run Qt
if runqt:
  qapp.exec_()
  
