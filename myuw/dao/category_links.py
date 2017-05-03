from django.db.models import Q
from myuw.models.res_category_link import ResCategoryLink
from myuw.dao.affiliation import get_base_campus, get_all_affiliations
import csv
import os


class Res_Links:
    """
    Read the resource links froma file and store them
    in an array of ResCategoryLink objects.
    """

    _singleton = None

    def __init__(self):
        self.links = []
        path = os.path.join(
            os.path.dirname(__file__),
            '..', 'data', 'category_links_import.csv')

        with open(path, 'rbU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            reader.next()
            for row in reader:
                category = row[0]
                category_id = _get_category_id(category)
                subcategory = row[1]
                affiliation = row[2]
                pce = row[3]
                central_url = row[4]
                central_title = row[5]
                seattle_url = row[6]
                seattle_title = row[7]
                bothell_url = row[8]
                bothell_title = row[9]
                tacoma_url = row[10]
                tacoma_title = row[11]

                new_tab = False
                if row[12] == "yes":
                    new_tab = True

                if len(central_url) > 0:
                    link = ResCategoryLink(
                        url=central_url,
                        title=central_title,
                        affiliation=affiliation + "+" + pce,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    self.links.append(link)

                if len(seattle_url) > 0:
                    link = ResCategoryLink(
                        url=seattle_url,
                        title=seattle_title,
                        affiliation=affiliation + "+" + pce,
                        campus=ResCategoryLink.SEATTLE,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    self.links.append(link)

                if len(bothell_url) > 0:
                    link = ResCategoryLink(
                        url=bothell_url,
                        title=bothell_title,
                        affiliation=affiliation + "+" + pce,
                        campus=ResCategoryLink.BOTHELL,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    self.links.append(link)

                if len(tacoma_url) > 0:
                    link = ResCategoryLink(
                        url=tacoma_url,
                        title=tacoma_title,
                        affiliation=affiliation + "+" + pce,
                        campus=ResCategoryLink.TACOMA,
                        category_name=category,
                        sub_category=subcategory,
                        new_tab=new_tab
                        )
                    link.set_category_id(category)
                    self.links.append(link)

    @classmethod
    def get_all_links(cls):
        if cls._singleton is None:
            cls._singleton = Res_Links()
        return cls._singleton.links


def _get_category_id(category_name):
    category_id = category_name.lower()
    category_id = "".join(c for c in category_id if c.isalpha())
    return category_id


def get_links_for_category(search_category_id, request):
    return _get_links_by_category_and_campus(search_category_id,
                                             get_base_campus(request),
                                             get_all_affiliations(request))


def _get_links_by_category_and_campus(search_category_id,
                                      campus,
                                      affiliations):
    selected_links = []
    all_links = Res_Links.get_all_links()

    for link in all_links:
        if not link.category_id_matched(search_category_id):
            continue

        if link.all_affiliation() and link.campus_matched(campus) and\
                _pce_match(link, affiliations):
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["grad"] and link.for_grad() and\
                _pce_match(link, affiliations):
            selected_links.append(link)
            continue

        if link.campus_matched(campus) and\
                affiliations["undergrad"] and\
                (link.for_undergrad() or link.for_fyp()) and\
                _pce_match(link, affiliations):
            selected_links.append(link)
            continue

    return selected_links


def _pce_match(link, affiliations):
    """
    Takes a ResCategoryLink and the user's affiliations, and then returns
    true if the link should be displayed according to the link and user's
    PCE status
    """
    return (link.for_pce() and affiliations['pce']) or not link.for_pce()
