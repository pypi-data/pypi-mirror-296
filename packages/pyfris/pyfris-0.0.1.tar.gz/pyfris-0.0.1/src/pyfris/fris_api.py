import requests
from bs4 import BeautifulSoup
from xml.dom import minidom
import json
import unicodedata
from pathlib import Path


vods_path = Path.home() / "Desktop" / "GitHub" / "pyfris" / "VODS_2018_WOS_ID.txt"


class FRIS_API:
    """Class for interacting with the FRIS API."""

    _instance = None
    _vods_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Loading VODS data...")
            cls._load_data()
            print("VODS data loaded.\n")
        else:
            print("\nVODS data already loaded.\n")
        return cls._instance

    @classmethod
    def _load_data(cls):
        with open(vods_path, "r") as f:
            cls._vods_data = json.load(f)

    def get_data(self):
        return self._vods_data

    def __init__(self):
        pass

    def ppxml(self, xml):
        """Pretty prints XML responses."""
        xml = minidom.parseString(xml)
        xml = xml.toprettyxml()
        print(xml)

    def search_projects(self, query: str, n: int = 10, verbose: bool = False):
        """Searches for projects given a query. min(n) = 10."""
        url = "https://frisr4.researchportal.be/ws/ProjectService?wsdl"

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ns1:getProjects xmlns:ns1="http://fris.ewi.be/">
                    <search.search>{query}</search.search>
                    <projectCriteria xmlns="http://fris.ewi.be/criteria">
                        <window>
                            <pageSize>{n}</pageSize>
                            <pageNumber>0</pageNumber>
                        </window>
                    </projectCriteria>
                </ns1:getProjects>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.request("POST", url, data=payload)
        soup = BeautifulSoup(response.text, "xml")

        if verbose:
            self.ppxml(response.text)

        projects_soup = soup.find_all(lambda tag: tag.name == "cfProj")

        # projects as ID, title pairs
        projects = {}
        for project in projects_soup:
            raw_id = project.find("cfProjId").text
            uuid = raw_id.split(":")[1] if ":" in raw_id else raw_id

            title = ""
            titles_soup = project.find_all(lambda tag: tag.name == "cfTitle")
            for t in titles_soup:
                if t["cfLangCode"] in ["en", "un"]:
                    t_html = BeautifulSoup(t.text, "html.parser")
                    title = t_html.get_text()
                    break
            if title == "":
                title_html = BeautifulSoup(titles_soup[0].text, "html.parser")
                title = title_html.get_text()
            title = unicodedata.normalize("NFKD", title)
            projects[uuid] = title
        return projects

    def search_pubs(self, query: str, n: int = 10, verbose: bool = False):
        """Searches for pubs given a query. min(n) = 10."""
        url = "https://frisr4.researchportal.be/ws/ResearchOutputService?wsdl"

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <getResearchOutput xmlns="http://fris.ewi.be/">
                    <search.search>{query}</search.search>
                    <researchOutputCriteria xmlns="http://fris.ewi.be/criteria">
                        <window>
                            <pageSize>{n}</pageSize>
                            <pageNumber>0</pageNumber>
                        </window>
                    </researchOutputCriteria>
                </getResearchOutput>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.request("POST", url, data=payload)
        soup = BeautifulSoup(response.text, "xml")

        if verbose:
            self.ppxml(response.text)

        pubs_soup = soup.find_all(lambda tag: tag.name == "cfResPubl")
        pubs_soup = [pub for pub in pubs_soup if pub.find("cfResPublDate")]

        # pubs as ID, title pairs
        pubs = {}
        for publication in pubs_soup:
            raw_id = publication.find("cfResPublId").text
            uuid = raw_id
            # uuid = raw_id.split(":")[1] if ":" in raw_id else raw_id

            title = ""
            titles_soup = publication.find_all(lambda tag: tag.name == "cfTitle")
            for t in titles_soup:
                if t["cfLangCode"] in ["en", "un"]:
                    t_html = BeautifulSoup(t.text, "html.parser")
                    title = t_html.get_text()
                    break
            if title == "":
                title_html = BeautifulSoup(titles_soup[0].text, "html.parser")
                title = title_html.get_text()
            title = unicodedata.normalize("NFKD", title)
            pubs[uuid] = title
        return pubs

    def get_pub_ids(self, uuid: str, verbose: bool = False):
        """Retrieves all publication IDs for a project given its UUID."""
        url = "https://frisr4.researchportal.be/ws/ResearchOutputService?wsdl"

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <getResearchOutput xmlns="http://fris.ewi.be/">
                    <researchOutputCriteria xmlns="http://fris.ewi.be/criteria">
                        <associatedProjects>
                            <identifier>{uuid}</identifier>
                        </associatedProjects>
                    </researchOutputCriteria>
                </getResearchOutput>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.request("POST", url, data=payload)

        soup = BeautifulSoup(response.text, "xml")
        results = soup.find_all(lambda tag: tag.name == "cfResPubl")
        pub_list = [
            result.find("cfResPublId").text
            for result in results
            if result.find("cfResPublDate")
        ]
        pub_ids = []
        for pub in pub_list:
            if ":" in pub:
                pub = pub.split(":")[1]
            pub_ids.append(pub)
        return pub_ids

    def get_project(self, uuid: str, verbose: bool = False):
        """Retrieves project information given its UUID."""
        url = "https://frisr4.researchportal.be/ws/ProjectService?wsdl"

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ns1:getProjects xmlns:ns1="http://fris.ewi.be/">
                    <projectCriteria xmlns="http://fris.ewi.be/criteria">
                        <uuids>
                            <identifier>{uuid}</identifier>
                        </uuids>
                    </projectCriteria>
                </ns1:getProjects>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.request("POST", url, data=payload)
        soup = BeautifulSoup(response.text, "xml")

        if verbose:
            self.ppxml(response.text)

        # title
        title = ""
        title_soup = soup.find_all(lambda tag: tag.name == "cfTitle")
        for t in title_soup:
            if t["cfLangCode"] in ["en", "un"]:
                title_html = BeautifulSoup(t.text, "html.parser")
                title = title_html.get_text()
                break
        if title == "":
            title_html = BeautifulSoup(title_soup[0].text, "html.parser")
            title = title_html.get_text()
        title = unicodedata.normalize("NFKD", title)

        # abstract
        abstract = ""
        abstract_soup = soup.find_all(lambda tag: tag.name == "cfAbstr")
        for a in abstract_soup:
            if a["cfLangCode"] in ["en", "un"]:
                abstract_html = BeautifulSoup(a.text, "html.parser")
                abstract = abstract_html.get_text()
                break
        if abstract == "":
            abstract_html = BeautifulSoup(abstract_soup[0].text, "html.parser")
            abstract = abstract_html.get_text()
        abstract = unicodedata.normalize("NFKD", abstract)

        # keywords
        keywords = []
        keywords_soup = soup.find_all(lambda tag: tag.name == "cfKeyw")
        for k in keywords_soup:
            if k["cfLangCode"] in ["en", "un"]:
                k_html = BeautifulSoup(k.text, "html.parser")
                keyword = unicodedata.normalize("NFKD", k_html.get_text())
                keywords.append(keyword)

        # start date, format: 2018-10-01T00:00:00.000Z
        start_date_soup = soup.find(lambda tag: tag.name == "cfProj")
        start_date = start_date_soup.find("cfStartDate").text[:10]

        # organization
        organizations_soup = soup.find_all(lambda tag: tag.name == "cfOrgUnitId")
        organizations = [organization.text for organization in organizations_soup]
        organizations = list(set(organizations))

        # disciplines
        pro_class_soup = soup.find_all(lambda tag: tag.name == "cfProj_Class")
        disciplines = []
        for pro_class in pro_class_soup:
            if pro_class.find("cfClassSchemeId").text == "Flemish Research Disciplines":
                disciplines.append(pro_class.find("cfClassId").text[:4])
        disciplines = sorted(list(set(disciplines)))

        # authors
        last_name_soup = soup.find_all(lambda tag: tag.name == "cfFamilyNames")
        first_name_soup = soup.find_all(lambda tag: tag.name == "cfFirstNames")
        authors = []
        for last_name, first_name in zip(last_name_soup, first_name_soup):
            authors.append(f"{first_name.text} {last_name.text}")
        authors = list(set(authors))

        # funding
        try:
            funding_soup = soup.find_all("cfFundId")
            funding_ids = [funding.text for funding in funding_soup]
            funding_ids = list(set(funding_ids))
        except:
            funding_ids = []

        return (
            title,
            abstract,
            keywords,
            disciplines,
            start_date,
            organizations,
            authors,
            funding_ids,
        )

    def get_publication(self, pub_id: str, verbose: bool = False):
        """Retrieves publication information given its ID."""
        url = "https://frisr4.researchportal.be/ws/ResearchOutputService?wsdl"

        payload = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <getResearchOutput xmlns="http://fris.ewi.be/">
                    <researchOutputCriteria xmlns="http://fris.ewi.be/criteria">
                        <uuids>
                            <identifier>{pub_id}</identifier>
                        </uuids>
                    </researchOutputCriteria>
                </getResearchOutput>
            </soap:Body>
        </soap:Envelope>
        """

        response = requests.request("POST", url, data=payload)
        soup = BeautifulSoup(response.text, "xml")

        if verbose:
            self.ppxml(response.text)

        # title
        title = ""
        title_soup = soup.find_all(lambda tag: tag.name == "cfTitle")
        for t in title_soup:
            if t["cfLangCode"] in ["en", "un"]:
                title_html = BeautifulSoup(t.text, "html.parser")
                title = title_html.get_text()
                break
        if title == "":
            title_html = BeautifulSoup(title_soup[0].text, "html.parser")
            title = title_html.get_text()
        title = unicodedata.normalize("NFKD", title)

        # abstract
        abstract = ""
        abstract_soup = soup.find_all(lambda tag: tag.name == "cfAbstr")
        for a in abstract_soup:
            if a["cfLangCode"] in ["en", "un"]:
                abstract_html = BeautifulSoup(a.text, "html.parser")
                abstract = abstract_html.get_text()
                break
        if abstract == "":
            abstract_html = BeautifulSoup(abstract_soup[0].text, "html.parser")
            abstract = abstract_html.get_text()
        abstract = unicodedata.normalize("NFKD", abstract)

        # keywords
        keywords = []
        keywords_soup = soup.find_all(lambda tag: tag.name == "cfKeyw")
        for k in keywords_soup:
            if k["cfLangCode"] in ["en", "un"]:
                k_html = BeautifulSoup(k.text, "html.parser")
                keyword = unicodedata.normalize("NFKD", k_html.get_text())
                keywords.append(keyword)

        # disciplines
        cfFedIds = soup.find_all("cfFedId")
        wos_id = None
        for fed in cfFedIds:
            try:
                if fed.find("cfClassId").text == "WoS Id":
                    wos_id = fed.find("cfFedId").text
            except:
                continue

        if wos_id:
            disciplines = sorted(self.get_data()[wos_id].split(","))
        else:
            disciplines = []

        # organizations
        organizations_soup = soup.find_all("cfOrgUnitId")
        organizations = [organization.text for organization in organizations_soup]
        organizations = list(set(organizations))

        # date, format: 2018-10-01Z
        start_dates_soup = soup.find_all("cfStartDate")
        start_dates = [start_date.text[:10] for start_date in start_dates_soup]
        start_date = sorted(start_dates)[0]

        # authors
        first_name_soup = soup.find_all(lambda tag: tag.name == "cfFirstNames")
        last_name_soup = soup.find_all(lambda tag: tag.name == "cfFamilyNames")
        authors = []
        for first_name, last_name in zip(first_name_soup, last_name_soup):
            authors.append(f"{first_name.text} {last_name.text}")
        authors = list(set(authors))

        # funding
        try:
            funding_soup = soup.find_all("cfFundId")
            funding_ids = [funding.text for funding in funding_soup]
            funding_ids = list(set(funding_ids))
        except:
            funding_ids = []

        return (
            title,
            abstract,
            keywords,
            disciplines,
            start_date,
            organizations,
            authors,
            funding_ids,
        )


if __name__ == "__main__":
    # fris = FRIS_API()
    # projects = fris.search_projects("protein", 10)
    # print(projects)
    # print(fris.search_pubs("protein", 10))
    # pro_id = list(projects.keys())[1]
    # pub_ids = fris.get_pub_ids(pro_id)
    # print(fris.get_project(pro_id))
    # print(pub_ids)
    # print(fris.get_publication(pub_ids[0]))
    # fris2 = FRIS_API()
    # print(fris2.get_publication(pub_ids[0]))

    fris = FRIS_API()
    fris2 = FRIS_API()
