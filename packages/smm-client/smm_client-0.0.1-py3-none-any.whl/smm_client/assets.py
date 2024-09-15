# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Assets
"""


class SMMAsset:
    """
    Search Management Map - Asset
    """

    def __init__(self, connection, asset_id: int, name: str):
        self.connection = connection
        self.id = asset_id
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"


class SMMAssetType:
    """
    Search Management Map - Asset Type
    """

    def __init__(self, connection, type_id: int, name: str):
        self.connection = connection
        self.id = type_id
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"
