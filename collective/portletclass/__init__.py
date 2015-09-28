from zope.i18nmessageid import MessageFactory
from zope.interface import implements, Interface
from Products.Five import BrowserView
from plone.app.portlets.portlets.navigation import Assignment as navigation_assignment

MessageFactory = MessageFactory('collective.portletclass')

class ICollectivePortletClassUtilities(Interface):

    def getPortletClass(self):
        pass

class CollectivePortletClassUtilities(BrowserView):

    implements(ICollectivePortletClassUtilities)

    def getPortletClass(self, assignment):
        klasses = []
        collective_portletclass = getattr(assignment, 'collective_portletclass', '')
        mobile_navigation = getattr(assignment, 'mobile_navigation', False)
        portlet_width = getattr(assignment, 'portlet_width', '')
        portlet_item_count = getattr(assignment, 'portlet_item_count', '')
        
        # Figure out if we are a navigation portlet in the left column, so we can
        # apply the 'mobile-navigation' class.
        
        is_nav_portlet = isinstance(assignment, navigation_assignment)
        is_left_column_nav_portlet = False
        
        if is_nav_portlet:
            try:
                if assignment.__parent__.__manager__ == 'plone.leftcolumn':
                    is_left_column_nav_portlet = True
            except:
                pass

        # These classes will have 'portlet-' prepended to them.

        if collective_portletclass:
            klasses.extend(collective_portletclass.split())

        if mobile_navigation or is_left_column_nav_portlet:
            klasses.append("mobile-navigation")

        # Do the prepending

        klasses = ["portlet-%s" % x for x in klasses]

        # These classes will *not* have 'portlet-' prepended to them.

        if portlet_width:
            klasses.append('tileitem-width-%s' % portlet_width)

        if portlet_item_count:
            klasses.append('tileitem-count-%s' % portlet_item_count)

        # Return space separated string

        if klasses:
            return ' ' + " ".join(klasses)
        else:
            return ""