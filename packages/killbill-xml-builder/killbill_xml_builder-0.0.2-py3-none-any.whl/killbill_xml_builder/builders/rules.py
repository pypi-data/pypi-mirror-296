from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.enums import (
    BillingPolicy,
    EntitlementPolicy,
    PhaseType,
    ProductCategory,
    BillingPeriod,
)


class ChangePolicyCase(Base):

    def __init__(
        self,
        policy: BillingPolicy,
        phase_type: PhaseType = None,
        from_product: Product = None,
        from_product_category: ProductCategory = None,
        from_billing_period: BillingPeriod = None,
        from_price_list: str = None,
        to_product: Product = None,
        to_product_category: ProductCategory = None,
        to_billing_period: BillingPeriod = None,
        to_price_list: str = None,
    ) -> None:
        """Create the XML representation of the change policy case"""
        self.policy = policy
        self.phase_type = phase_type
        self.from_product = from_product
        self.from_product_category = from_product_category
        self.from_billing_period = from_billing_period
        self.from_price_list = from_price_list
        self.to_product = to_product
        self.to_product_category = to_product_category
        self.to_billing_period = to_billing_period
        self.to_price_list = to_price_list
        self.to_xml()

    def to_xml(self):
        
        root = ET.Element("changePolicyCase")

        if self.phase_type:
            phase_type_element = ET.SubElement(root, "phaseType")
            phase_type_element.text = str(self.phase_type)

        if self.from_product:
            from_product_element = ET.SubElement(root, "fromProduct")
            from_product_element.text = self.from_product.name

        if self.from_product_category:
            from_product_category_element = ET.SubElement(root, "fromProductCategory")
            from_product_category_element.text = str(self.from_product_category)

        if self.from_billing_period:
            from_billing_period_element = ET.SubElement(root, "fromBillingPeriod")
            from_billing_period_element.text = str(self.from_billing_period)

        if self.from_price_list:
            from_price_list_element = ET.SubElement(root, "fromPriceList")
            from_price_list_element.text = self.from_price_list

        if self.to_product:
            to_product_element = ET.SubElement(root, "toProduct")
            to_product_element.text = self.to_product.name

        if self.to_product_category:
            to_product_category_element = ET.SubElement(root, "toProductCategory")
            to_product_category_element.text = str(self.to_product_category)

        if self.to_billing_period:
            to_billing_period_element = ET.SubElement(root, "toBillingPeriod")
            to_billing_period_element.text = str(self.to_billing_period)

        if self.to_price_list:
            to_price_list_element = ET.SubElement(root, "toPriceList")
            to_price_list_element.text = self.to_price_list

        policy_element = ET.SubElement(root, "policy")
        policy_element.text = str(self.policy)

        self.element = root


class CancelPolicyCase(Base):

    def __init__(
        self, policy: EntitlementPolicy, product_category: ProductCategory = None
    ) -> None:
        """Create the XML representation of the cancel policy case"""
        self.policy = policy
        self.product_category = product_category
        self.to_xml()

    def to_xml(self):

        root = ET.Element("cancelPolicyCase")

        if self.product_category:
            product_category_element = ET.SubElement(root, "productCategory")
            product_category_element.text = str(self.product_category)

        policy_element = ET.SubElement(root, "policy")
        policy_element.text = str(self.policy)

        self.element = root


class Rules(Base):

    def __init__(
        self,
        change_policy_cases: List[ChangePolicyCase],
        cancel_policy_cases: List[CancelPolicyCase],
    ) -> None:
        """Create the XML representation of the rule"""

        self.change_policy_cases = change_policy_cases
        self.cancel_policy_cases = cancel_policy_cases
        self.to_xml()

    def to_xml(self):

        root = ET.Element("rules")

        if self.change_policy_cases:

            change_policy_element = ET.SubElement(root, "changePolicy")
            for cpc in self.change_policy_cases:
                change_policy_element.append(cpc.element)

        if self.cancel_policy_cases:
            cancel_policy_element = ET.SubElement(root, "cancelPolicy")
            for cpc in self.cancel_policy_cases:
                cancel_policy_element.append(cpc.element)

        self.element = root
