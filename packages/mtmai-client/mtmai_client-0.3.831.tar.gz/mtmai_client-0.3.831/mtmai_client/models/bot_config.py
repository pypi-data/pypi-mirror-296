from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BotConfig")


@_attrs_define
class BotConfig:
    """mtmaibot 配置

    Attributes:
        base_url (str):
        api_prefix (str):
        access_token (str):
        login_url (str):
    """

    base_url: str
    api_prefix: str
    access_token: str
    login_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url

        api_prefix = self.api_prefix

        access_token = self.access_token

        login_url = self.login_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "baseUrl": base_url,
                "apiPrefix": api_prefix,
                "accessToken": access_token,
                "loginUrl": login_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("baseUrl")

        api_prefix = d.pop("apiPrefix")

        access_token = d.pop("accessToken")

        login_url = d.pop("loginUrl")

        bot_config = cls(
            base_url=base_url,
            api_prefix=api_prefix,
            access_token=access_token,
            login_url=login_url,
        )

        bot_config.additional_properties = d
        return bot_config

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
