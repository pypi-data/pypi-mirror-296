from src.pyfris import fris_api
import unittest


class TestFrisApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFrisApi, self).__init__(*args, **kwargs)
        self.fris = fris_api.FRIS_API()

    def test_search_projects(self):
        self.assertEqual(
            self.fris.search_projects("protein", 10),
            {
                "13443d2f-21b5-4445-ab31-3463c894bbb1": "Integration of high-detail-three-dimensional anatomical evaluation of the atrium with functional and metabolic factors to improve safety and effectiveness of catheter ablation of supraventricular arrhythmias",
                "d08ee64f-3200-4385-a8d9-b791620f0d15": "Heterogeneity and tissue imprinting of intestinal resident macrophages revisited: from transcriptome to function",
                "64e73430-db80-4915-88c1-4f95d8b874f2": "Relation between nanostructure of pectin and its functional properties, based on interaction with metalions.",
                "fcdca96e-6a7e-4c9d-a83f-a7e0cd13ea77": "A generic approach for uncertainty quantification in stereovision DIC",
                "061fbee2-17be-464d-b5b2-79271bae2d3b": "Syndecan-PDZ scaffolds in the molecular and functional heterogeneity of extracellular vesicles: the role of syntenin in ncRNA transfer",
                "696cbc79-3595-493b-a757-a8b355622612": "Encompassing flexible mean and quantile regression.",
                "fc18eb06-55a6-4781-81cd-76e700580f9c": "Capillary instability and interface dynamics of wetting states in binary mixtures of ultra-cold gases.",
                "022d88c0-a32f-452b-8aa6-d8f8135d0d45": "Statistical mechanics of inhomogeneous complex fluids and particle transport models",
                "f4df85ba-71d3-4486-a434-529e3ddc60a2": "Multi-scale monitoring and modelling for the analysis of the hydrologic response of southern Ecuadorian Andean páramos",
                "c6f1bd68-77aa-43e1-8755-2f6da633cd2a": "The Risk Management of Contingent Convertible (CoCo) Bonds",
            },
        )

    def test_search_pubs(self):
        self.assertEqual(
            self.fris.search_pubs("protein", 10),
            {
                "a1e556ce-4170-4f65-b7c9-0ec2cdd7ce83": "Image based flow analysis of microscale biological systems",
                "51fadf53-5966-4081-a67b-04009fbfbe92": "Enhanced liver fibrosis score correlates with transient elastography in patients with treated autoimmune hepatitis",
                "251fca8e-2a7a-4a3f-970e-034f9bda1e3c": "Long-term obeticholic acid (OCA) for primary biliary cholangitis (PBC) in a clinical trial improved event free survival (death, liver transplant and hepatic decompensation) compared to external controls from the GLOBAL PBC real-world database",
                "80eab9a3-205e-478a-b088-c6cb45eb3085": "A multicentric study to estimate mortality and graft loss risk after liver transplantation (LT) in patients with recurrent primary biliary cholangitis (PBC)",
                "8c1dd9fb-f294-46f3-915c-66711826421a": "Cross sections of deuteron induced nuclear reactions on metal targets",
                "189d9950-2eb6-497b-9ee1-2025c5c0d651": "Emotiecoachen in de wedstrijdsport. Driftkikkers en angsthazen",
                "18a2345e-649d-443e-8826-dc3495ece723": "Bending of nanoscale filament assemblies by elastocapillary densification",
                "18a725de-b3e7-413c-a351-c5f576512e67": "Sentence compression for Dutch using integer linear programming",
                "18a76b92-a4b7-4350-9d4d-b7d4f99673a5": "A new control structure to reduce time delay of tracking sensors by applying an angular position sensor",
                "18a93732-5498-4544-a506-072b1b4f11af": "Evaluation of Cardiac Function in Women With a History of Preeclampsia: A Systematic Review and Meta-Analysis",
            },
        )

    def test_get_pub_ids(self):
        pro_id = "d08ee64f-3200-4385-a8d9-b791620f0d15"
        self.assertEqual(
            self.fris.get_pub_ids(pro_id), ["e666abae-9f3e-4859-8105-64f2b51d00bc"]
        )

    def test_get_project(self):
        pro_id = "d08ee64f-3200-4385-a8d9-b791620f0d15"
        self.assertEqual(
            self.fris.get_project(pro_id),
            (
                "Heterogeneity and tissue imprinting of intestinal resident macrophages revisited: from transcriptome to function",
                "Intestinal macrophages are essential components of the gastrointestinal tract and exhibit highly specific functions depending on their anatomical location within the gut. Lamina propria macrophages face the gut lumen and are involved in bacterial clearance, initiation of adaptive immunity and installing oral tolerance. In contract, macrophages residing in the muscularis externa regulate intestinal peristaltic activity through direct crosstalk with enteric neurons. Increasing evidence from our group and others indeed suggests that the enteric nervous system (ENS) provides signals that account for the gut-specific macrophage phenotype. This tolerogenic transcriptome is characterized by an immunological quiescent state and linked to the prominent expression of the chemokine receptor CX3CR1 and other unique signature genes.However, the mediator(s) released by the enteric neurons determining the tolerogenic phenotype are unexplored. Moreover, revealing this neuro-modulated macrophage population has been complicated by the heterogeneity of hematopoietic cells within the gastrointestinal tract. This dissertation is focused on the comprehensive characterization of the intestinal macrophage population involved in the communication with enteric neurons. ENS-derived signals that shape macrophage identity will be explored and we will investigate how the macrophage-enteric neuronal crosstalk reflects in both physiological (such as intestinal motility) and disease contexts (such as DSS colitis and post-operative ileus).",
                ["Macrofage", "Intestinal homeostasis", "neuro-immune interactions"],
                ["0301", "0305", "0306"],
                "2014-10-01",
                ["f5af8a62-9241-49f1-bd56-a0aea67c9fce"],
                [],
                ["1000"],
            ),
        )

    def test_get_publication(self):
        pub_id = "e666abae-9f3e-4859-8105-64f2b51d00bc"
        self.assertEqual(
            self.fris.get_publication(pub_id),
            (
                "Heterogeneity and tissue imprinting of intestinal resident macrophages revisited: from transcriptome to function",
                "Intestinal macrophages are essential components of the gastrointestinal tract and exhibit highly specific functions depending on their anatomical location within the gut. Lamina propria macrophages face the gut lumen and are involved in bacterial clearance, initiation of adaptive immunity and installing oral tolerance. In contract, macrophages residing in the muscularis externa regulate intestinal peristaltic activity through direct crosstalk with enteric neurons. Increasing evidence from our group and others indeed suggests that the enteric nervous system (ENS) provides signals that account for the gut-specific macrophage phenotype. This tolerogenic transcriptome is characterized by an immunological quiescent state and linked to the prominent expression of the chemokine receptor CX3CR1 and other unique signature genes.However, the mediator(s) released by the enteric neurons determining the tolerogenic phenotype are unexplored. Moreover, revealing this neuro-modulated macrophage population has been complicated by the heterogeneity of hematopoietic cells within the gastrointestinal tract. This dissertation is focused on the comprehensive characterization of the intestinal macrophage population involved in the communication with enteric neurons. ENS-derived signals that shape macrophage identity will be explored and we will investigate how the macrophage-enteric neuronal crosstalk reflects in both physiological (such as intestinal motility) and disease contexts (such as DSS colitis and post-operative ileus).",
                [],
                [],
                "2007-10-01",
                ["f5af8a62-9241-49f1-bd56-a0aea67c9fce"],
                [],
                [],
            ),
        )