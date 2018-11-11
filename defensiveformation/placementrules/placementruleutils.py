from defensiveformation.placementrules.alignmentplacementrule import AlignmentPlacementRule, AlignmentPlacementRuleGUI
from defensiveformation.placementrules.conditionalplacementrule import ConditionalPlacementRule, \
    ConditionalPlacementRuleGUI
from defensiveformation.placementrules.overplacementrule import OverPlacementRule, OverPlacementRuleGUI


placement_type_dict = {
                'Alignment': AlignmentPlacementRule,
                'Over': OverPlacementRule,
                'Conditional': ConditionalPlacementRule
                }

placement_type_gui_dict = {
                AlignmentPlacementRule: AlignmentPlacementRuleGUI,
                OverPlacementRule: OverPlacementRuleGUI,
                ConditionalPlacementRule: ConditionalPlacementRuleGUI
                }

placement_type_name_dict = {
                AlignmentPlacementRule: 'Alignment',
                OverPlacementRule: 'Over',
                ConditionalPlacementRule: 'Conditional'
                }