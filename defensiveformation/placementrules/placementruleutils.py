from defensiveformation.placementrules.alignmentplacementrule import AlignmentPlacementRule, AlignmentPlacementRuleGUI
from defensiveformation.placementrules.apexplacementrule import ApexPlacementRule, ApexPlacementRuleGUI
from defensiveformation.placementrules.conditionalplacementrule import ConditionalPlacementRule, ConditionalPlacementRuleGUI
from defensiveformation.placementrules.overplacementrule import OverPlacementRule, OverPlacementRuleGUI


placement_type_dict = {
                'Alignment': AlignmentPlacementRule,
                'Over': OverPlacementRule,
                'Apex': ApexPlacementRule,
                'Conditional': ConditionalPlacementRule
                }

placement_type_gui_dict = {
                AlignmentPlacementRule: AlignmentPlacementRuleGUI,
                OverPlacementRule: OverPlacementRuleGUI,
                ApexPlacementRule: ApexPlacementRuleGUI,
                ConditionalPlacementRule: ConditionalPlacementRuleGUI
                }

placement_type_name_dict = {
                AlignmentPlacementRule: 'Alignment',
                OverPlacementRule: 'Over',
                ApexPlacementRule: 'Apex',
                ConditionalPlacementRule: 'Conditional'
                }