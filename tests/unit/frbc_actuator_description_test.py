

    from s2python.frbc import *
    from s2python.

    class FRBCActuatorDescriptionTest(TestCase):
        def test__from_json__happy_path_full(self):
            # Arrange
            json_str = """
    {
    "id": "f87e77fa-b984-4f9e-a1bf-a4782b600508",
    "diagnostic_label": "some-test-string7553",
    "supported_commodities": [
        "GAS"
    ],
    "operation_modes": [
        {
            "id": "93a450ba-c94c-46e4-8bae-b768c5867075",
            "diagnostic_label": "some-test-string64",
            "elements": [
                {
                    "fill_level_range": {
                        "start_of_range": 6056.10613410257,
                        "end_of_range": 37655.606469064296
                    },
                    "fill_rate": {
                        "start_of_range": 24637.49716859664,
                        "end_of_range": 29714.5724875526
                    },
                    "power_ranges": [
                        {
                            "start_of_range": 25430.49420136962,
                            "end_of_range": 65352.058496320744,
                            "commodity_quantity": "ELECTRIC.POWER.L1"
                        }
                    ],
                    "running_costs": {
                        "start_of_range": 5704.446007733921,
                        "end_of_range": 20299.76272470042
                    }
                }
            ],
            "abnormal_condition_only": false
        }
    ],
    "transitions": [
        {
            "id": "e5a850b3-cfa9-49c6-aec7-3658d59fdadc",
            "from_": "5df9e140-7486-4cbe-b6cb-950e9010ef27",
            "to": "0246915c-bcd1-4d6e-90bd-e97dbd2de803",
            "start_timers": [
                "18c556e0-9a56-4aa3-9535-acc2440371ff"
            ],
            "blocking_timers": [
                "e0269765-8eb8-46b6-8ef1-4fa7df853b0c"
            ],
            "transition_costs": 5373.494383957436,
            "transition_duration": 31883,
            "abnormal_condition_only": false
        }
    ],
    "timers": [
        {
            "id": "89ff3d76-6e22-4436-a885-b7e868b5b246",
            "diagnostic_label": "some-test-string6221",
            "duration": 33492
        }
    ]
}
            """

            # Act
            frbc_actuator_description = FRBCActuatorDescription.from_json(json_str)

            # Assert
            self.assertEqual(frbc_actuator_description.id, uuid.UUID("f87e77fa-b984-4f9e-a1bf-a4782b600508"))
        self.assertEqual(frbc_actuator_description.diagnostic_label, "some-test-string7553")
        self.assertEqual(frbc_actuator_description.supported_commodities, [Commodity.GAS])
        self.assertEqual(frbc_actuator_description.operation_modes, [FRBCOperationMode(id=uuid.UUID("93a450ba-c94c-46e4-8bae-b768c5867075"), diagnostic_label="some-test-string64", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=6056.10613410257, end_of_range=37655.606469064296), fill_rate=NumberRange(start_of_range=24637.49716859664, end_of_range=29714.5724875526), power_ranges=[PowerRange(start_of_range=25430.49420136962, end_of_range=65352.058496320744, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=5704.446007733921, end_of_range=20299.76272470042))], abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.transitions, [Transition(id=uuid.UUID("e5a850b3-cfa9-49c6-aec7-3658d59fdadc"), from_=uuid.UUID("5df9e140-7486-4cbe-b6cb-950e9010ef27"), to=uuid.UUID("0246915c-bcd1-4d6e-90bd-e97dbd2de803"), start_timers=[uuid.UUID("18c556e0-9a56-4aa3-9535-acc2440371ff")], blocking_timers=[uuid.UUID("e0269765-8eb8-46b6-8ef1-4fa7df853b0c")], transition_costs=5373.494383957436, transition_duration=Duration.from_timedelta(timedelta(milliseconds=31883)), abnormal_condition_only=False)])
        self.assertEqual(frbc_actuator_description.timers, [Timer(id=uuid.UUID("89ff3d76-6e22-4436-a885-b7e868b5b246"), diagnostic_label="some-test-string6221", duration=Duration.from_timedelta(timedelta(milliseconds=33492)))])

        def test__to_json__happy_path_full(self):
            # Arrange
            frbc_actuator_description = FRBCActuatorDescription(id=uuid.UUID("f87e77fa-b984-4f9e-a1bf-a4782b600508"), diagnostic_label="some-test-string7553", supported_commodities=[Commodity.GAS], operation_modes=[FRBCOperationMode(id=uuid.UUID("93a450ba-c94c-46e4-8bae-b768c5867075"), diagnostic_label="some-test-string64", elements=[FRBCOperationModeElement(fill_level_range=NumberRange(start_of_range=6056.10613410257, end_of_range=37655.606469064296), fill_rate=NumberRange(start_of_range=24637.49716859664, end_of_range=29714.5724875526), power_ranges=[PowerRange(start_of_range=25430.49420136962, end_of_range=65352.058496320744, commodity_quantity=CommodityQuantity.ELECTRIC_POWER_L1)], running_costs=NumberRange(start_of_range=5704.446007733921, end_of_range=20299.76272470042))], abnormal_condition_only=False)], transitions=[Transition(id=uuid.UUID("e5a850b3-cfa9-49c6-aec7-3658d59fdadc"), from_=uuid.UUID("5df9e140-7486-4cbe-b6cb-950e9010ef27"), to=uuid.UUID("0246915c-bcd1-4d6e-90bd-e97dbd2de803"), start_timers=[uuid.UUID("18c556e0-9a56-4aa3-9535-acc2440371ff")], blocking_timers=[uuid.UUID("e0269765-8eb8-46b6-8ef1-4fa7df853b0c")], transition_costs=5373.494383957436, transition_duration=Duration.from_timedelta(timedelta(milliseconds=31883)), abnormal_condition_only=False)], timers=[Timer(id=uuid.UUID("89ff3d76-6e22-4436-a885-b7e868b5b246"), diagnostic_label="some-test-string6221", duration=Duration.from_timedelta(timedelta(milliseconds=33492)))])

            # Act
            json_str = frbc_actuator_description.to_json()

            # Assert
            expected_json = {   'diagnostic_label': 'some-test-string7553',
    'id': 'f87e77fa-b984-4f9e-a1bf-a4782b600508',
    'operation_modes': [   {   'abnormal_condition_only': False,
                               'diagnostic_label': 'some-test-string64',
                               'elements': [   {   'fill_level_range': {   'end_of_range': 37655.606469064296,
                                                                           'start_of_range': 6056.10613410257},
                                                   'fill_rate': {   'end_of_range': 29714.5724875526,
                                                                    'start_of_range': 24637.49716859664},
                                                   'power_ranges': [   {   'commodity_quantity': 'ELECTRIC.POWER.L1',
                                                                           'end_of_range': 65352.058496320744,
                                                                           'start_of_range': 25430.49420136962}],
                                                   'running_costs': {   'end_of_range': 20299.76272470042,
                                                                        'start_of_range': 5704.446007733921}}],
                               'id': '93a450ba-c94c-46e4-8bae-b768c5867075'}],
    'supported_commodities': ['GAS'],
    'timers': [   {   'diagnostic_label': 'some-test-string6221',
                      'duration': 33492,
                      'id': '89ff3d76-6e22-4436-a885-b7e868b5b246'}],
    'transitions': [   {   'abnormal_condition_only': False,
                           'blocking_timers': [   'e0269765-8eb8-46b6-8ef1-4fa7df853b0c'],
                           'from_': '5df9e140-7486-4cbe-b6cb-950e9010ef27',
                           'id': 'e5a850b3-cfa9-49c6-aec7-3658d59fdadc',
                           'start_timers': [   '18c556e0-9a56-4aa3-9535-acc2440371ff'],
                           'to': '0246915c-bcd1-4d6e-90bd-e97dbd2de803',
                           'transition_costs': 5373.494383957436,
                           'transition_duration': 31883}]}
            self.assertEqual(json.loads(json_str), expected_json)
    