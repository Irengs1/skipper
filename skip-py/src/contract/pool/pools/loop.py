from dataclasses import dataclass

from src.contract.pool.pools import Terraswap
from src.querier import Querier


@dataclass
class Loop(Terraswap):
    DEFAULT_FEE_FROM_INPUT: bool = False
    
    async def update_fees(self, querier: Querier) -> None:
        fee_info_payload = self.get_query_fees_payload(
                                    contract_address=self.contract_address,
                                    querier=querier)   
        
        fee_info = await querier.query_node_and_return_response(
                                        payload=fee_info_payload,
                                        decoded=True
                                        )
        fee = float(fee_info['commission_rate'])
        
        extra_commission_info_payload = self.get_extra_commission_info_payload(
                                                    contract_address=self.contract_address,
                                                    querier=querier
                                                    )

        extra_commission_info = await querier.query_node_and_return_response(
                                                    payload=extra_commission_info_payload,
                                                    decoded=True
                                                    )
        fee_allocation = float(extra_commission_info["fee_allocation"])
        
        self.protocol_fee = fee * (fee_allocation / 100)
        self.lp_fee = fee - self.protocol_fee
        self.fee_from_input = self.DEFAULT_FEE_FROM_INPUT
    
    @staticmethod
    def get_query_fees_payload(contract_address: str, querier: Querier) -> dict:
        return querier.create_payload(contract_address, {"query_config":{}})

    @staticmethod
    def get_extra_commission_info_payload(contract_address: str, querier: Querier) -> dict:
        return querier.create_payload(contract_address, {"extra_commission_info":{}})