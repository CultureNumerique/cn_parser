#!/usr/bin/python
# coding: utf8


import unittest
from io import StringIO
import os
import logging
from pygiftparser import parser as pygift
from cnparser import model, toIMS, fromGift
from cnparser.cnsettings import IMS_DIRECTORY, FOLDERS
# Ignore Warning
logger = logging.getLogger()
logger.setLevel(40)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


TEST_OUT_DIR = "./outTestIMS"
TEST_IMS_DIR = os.path.join(TEST_OUT_DIR, IMS_DIRECTORY)


class IMSQuestionsTestCase(unittest.TestCase):

    def setUp(self):
        """
        Build IMS folder based on coursTest
        """
        io_ourQuestions = StringIO("""
::MULTIANSWER::
What two people are entombed in Grant's tomb? {
~%-100%No one
~%50%Grant #One comment
~%50%Grant's wife
~%-100%Grant's father
}

::TRUEFALSE1::
Vrai ou Faux?
{T #Non...#Exact !
####MEGA COMMENT
}

::TRUEFALSE2::
Faux ou Vrai?
{F #Pas bon...#C'est ça!
}

::SINGLEANSWER::
Question {
=A correct answer
~Wrong answer1
#A response to wrong
~Wrong answer2
#A response to wrong
~Wrong answer3
#A response to wrong
~Wrong answer4
#A response to wrong
}

::ESSAY::
Blablablabla {
#### MEGA COMMENT
}
        """)

        self.questions = pygift.parseFile(io_ourQuestions)

    def testHeader(self):
        """
        """

        ims = toIMS.create_ims_test(self.questions, '1', 'multi')
        self.assertTrue('<?xml version="1.0" encoding="UTF-8"?>'.strip() in ims.strip())
        self.assertTrue("""<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemalocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_qtiasiv1p2p1_v1p0.xsd">""".strip() in ims.strip())

        # ALL
        # Rewrite: not guaranty on order!!!
    #     self.assertTrue("""<qtimetadata>
    #   <qtimetadatafield>
    #     <fieldlabel>qmd_scoretype</fieldlabel>
    #     <fieldentry>Percentage</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>qmd_hintspermitted</fieldlabel>
    #     <fieldentry>Yes</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>qmd_feedbackpermitted</fieldlabel>
    #     <fieldentry>Yes</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>cc_profile</fieldlabel>
    #     <fieldentry>cc.exam.v0p1</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>cc_maxattempts</fieldlabel>
    #     <fieldentry>1</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>qmd_assessmenttype</fieldlabel>
    #     <fieldentry>Examination</fieldentry>
    #   </qtimetadatafield>
    #   <qtimetadatafield>
    #     <fieldlabel>qmd_solutionspermitted</fieldlabel>
    #     <fieldentry>Yes</fieldentry>
    #   </qtimetadatafield>
    # </qtimetadata>""".strip() in ims.strip())

        self.assertTrue("""<rubric>
      <material label="Summary">
        <mattext texttype="text/html"></mattext>
      </material>
    </rubric>""".strip() in ims.strip())

    def testMulti(self):
        """
        """

        multi = self.questions[0]
        imsmulti = toIMS.create_ims_test([multi], '1', 'multi')
        # print(imsmulti.strip())
        self.assertTrue("""<section ident="section_1_test_1">
      <item ident="q_0" title="MULTIANSWER">""".strip() in imsmulti.strip())
        self.assertTrue("""<itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_response.v0p1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_question_category</fieldlabel>
              <fieldentry>Quiz Bank multi</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>""".strip() in imsmulti.strip())
        self.assertTrue("""<presentation>
          <material>
            <mattext texttype="text/html">&lt;p&gt; What two people are entombed in Grant's tomb?&lt;/p&gt;</mattext>
          </material>""".strip() in imsmulti.strip())
        # imstree = etree.fromstring(unidecode.unidecode(imsmulti))
        # self.assertTrue("""<material>
        #           <mattext texttype="text/html">&lt;p&gt;No one&lt;/p&gt;</mattext>
        #         </material>""".strip() in imsmulti.strip())
        # self.assertTrue("""<material>
        #           <mattext texttype="text/html">&lt;p&gt;Grant&lt;/p&gt;</mattext>
        #         </material>""".strip() in imsmulti.strip())
        # self.assertTrue("""<material>
        #           <mattext texttype="text/html">&lt;p&gt;Grant's wife&lt;/p&gt;</mattext>
        #         </material>""".strip() in imsmulti.strip())
        # self.assertTrue("""<material>
        #           <mattext texttype="text/html">&lt;p&gt;Grant's father&lt;/p&gt;</mattext>
        #         </material>
        #       </response_label>
        #     </render_choice>
        #   </response_lid>
        # </presentation>""".strip() in imsmulti.strip())
        self.assertTrue("""<resprocessing>
          <outcomes>
            <decvar varname="SCORE" vartype="Decimal" maxvalue="100" minvalue="0" />
          </outcomes>
          <respcondition continue="No" title="Correct">
            <conditionvar>
              <and>""".strip() in imsmulti.strip())

        self.assertTrue("""<setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_fb" />
          </respcondition>""".strip() in imsmulti.strip())

        self.assertTrue("""<displayfeedback feedbacktype="Response" linkrefid="feedb_3" />
          </respcondition>
        </resprocessing>
        <itemfeedback ident="feedb_0">
          <flow_mat>
            <material>
              <mattext texttype="text/html"></mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_1">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;One comment&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_2">
          <flow_mat>
            <material>
              <mattext texttype="text/html"></mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_3">
          <flow_mat>
            <material>
              <mattext texttype="text/html"></mattext>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>
    </section>
  </assessment>
</questestinterop>""".strip() in imsmulti.strip())

    def testSingleAnswer(self):
        """
        """
        sglans = self.questions[3]
        imssglans = toIMS.create_ims_test([sglans], '4', 'sglans')

        # SINGLEANSWER
        # print(imssglans)
        self.assertTrue("""<section ident="section_1_test_4">
      <item ident="q_0" title="SINGLEANSWER">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_choice.v0p1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_question_category</fieldlabel>
              <fieldentry>Quiz Bank sglans</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>""".strip() in imssglans.strip())
        self.assertTrue("""<resprocessing>
          <outcomes>
            <decvar varname="SCORE" vartype="Decimal" maxvalue="100" minvalue="0" />
          </outcomes>
          <respcondition title="Correct">""".strip() in imssglans.strip())
        self.assertTrue("""<itemfeedback ident="feedb_0">
          <flow_mat>
            <material>
              <mattext texttype="text/html"></mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_1">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;A response to wrong&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_2">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;A response to wrong&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_3">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;A response to wrong&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
        <itemfeedback ident="feedb_4">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt;A response to wrong&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>
    </section>
  </assessment>
</questestinterop>""".strip() in imssglans.strip())

    def testTrueFalse(self):
        """
        """
        trfl = self.questions[1]
        imstrfl = toIMS.create_ims_test([trfl], '2', 'trfl')

        trfl2 = self.questions[2]
        imstrfl2 = toIMS.create_ims_test([trfl2], '3', 'trfl2')

        # TRUE FALSE FEEDBACK
        # print(imstrfl)
        self.assertTrue("""<section ident="section_1_test_2">
      <item ident="q_0" title="TRUEFALSE1">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_choice.v0p1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_question_category</fieldlabel>
              <fieldentry>Quiz Bank trfl</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        """.strip() in imstrfl.strip())

        self.assertTrue("""<presentation>
          <material>
            <mattext texttype="text/html">&lt;p&gt; Vrai ou Faux?&lt;/p&gt;</mattext>
        """.strip() in imstrfl.strip())

        self.assertTrue("""<resprocessing>
          <outcomes>
            <decvar varname="SCORE" vartype="Decimal" maxvalue="100" minvalue="0" />
          </outcomes>
          <respcondition continue="Yes" title="General feedback">
            <conditionvar>
              <other />
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_fb" />
          </respcondition>
        """)

        self.assertTrue("""<itemfeedback ident="general_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt; MEGA COMMENT&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>
    </section>
  </assessment>
</questestinterop>
        """.strip() in imstrfl.strip())

        # TRUE FALSE WITHOUT feedback
        # print(imstrfl2)
        self.assertTrue("""<section ident="section_1_test_3">
      <item ident="q_0" title="TRUEFALSE2">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.multiple_choice.v0p1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_question_category</fieldlabel>
              <fieldentry>Quiz Bank trfl2</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">&lt;p&gt; Faux ou Vrai?&lt;/p&gt;</mattext>
          </material>
        """.strip() in imstrfl2.strip())

        self.assertTrue("""</presentation>
        <resprocessing>
          <outcomes>
            <decvar varname="SCORE" vartype="Decimal" maxvalue="100" minvalue="0" />
          </outcomes>
          <respcondition title="">
        """.strip() in imstrfl2.strip())

        self.assertTrue("""<setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="feedb_1" />
          </respcondition>
        </resprocessing>
      </item>
    </section>
  </assessment>
</questestinterop>
        """.strip() in imstrfl2.strip())

    def testEssay(self):
        essay = self.questions[4]
        imsessay = toIMS.create_ims_test([essay], '5', 'essay')

        # ESSAY
        # print(imsessay)
        self.assertTrue("""<section ident="section_1_test_5">
      <item ident="q_0" title="ESSAY">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>cc_profile</fieldlabel>
              <fieldentry>cc.essay.v0p1</fieldentry>
            </qtimetadatafield>
            <qtimetadatafield>
              <fieldlabel>cc_question_category</fieldlabel>
              <fieldentry>Quiz Bank essay</fieldentry>
            </qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        """.strip() in imsessay.strip())

        self.assertTrue("""<itemfeedback ident="general_fb">
          <flow_mat>
            <material>
              <mattext texttype="text/html">&lt;p&gt; MEGA COMMENT&lt;/p&gt;</mattext>
            </material>
          </flow_mat>
        </itemfeedback>
      </item>
    </section>
  </assessment>
</questestinterop>
        """.strip() in imsessay.strip())


# Main
if __name__ == '__main__':
    unittest.main(verbosity=1)
