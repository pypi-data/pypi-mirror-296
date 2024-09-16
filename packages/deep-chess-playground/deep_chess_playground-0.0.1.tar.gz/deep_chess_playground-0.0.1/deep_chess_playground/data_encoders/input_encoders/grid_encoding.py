import chess
import torch
from typing import Dict, Any


class GridEncoder:
    def __init__(self, piece_channels: int = 12, control_channels: int = 12,
                 castling_channels: int = 4, pin_channels: int = 2):
        self.piece_channels = piece_channels
        self.control_channels = control_channels
        self.castling_channels = castling_channels
        self.pin_channels = pin_channels
        self.total_channels = (piece_channels + control_channels +
                               castling_channels + pin_channels)

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'GridEncoder':
        """
        Create a GridEncoder instance from a dictionary configuration.

        Args:
            config (Dict[str, Any]): A dictionary containing configuration parameters.

        Returns:
            GridEncoder: An instance of GridEncoder.

        Example:
            >>> config = {"piece_channels": 12, "control_channels": 12,
            ...           "castling_channels": 4, "pin_channels": 2}
            >>> encoder = GridEncoder.from_dict(config)
        """
        return cls(**config)

    @classmethod
    def from_json(cls, json_string: str) -> 'GridEncoder':
        """
        Create a GridEncoder instance from a JSON string configuration.

        Args:
            json_string (str): A JSON string containing configuration parameters.

        Returns:
            GridEncoder: An instance of GridEncoder.

        Example:
            >>> json_config = '{"piece_channels": 12, "control_channels": 12,
            ...                 "castling_channels": 4, "pin_channels": 2}'
            >>> encoder = GridEncoder.from_json(json_config)
        """
        import json
        config = json.loads(json_string)
        return cls.from_dict(config)

    def encode(self, board: chess.Board) -> torch.Tensor:
        """
        Encode the given chess board into a tensor representation.

        Args:
            board (chess.Board): The chess board to encode.

        Returns:
            torch.Tensor: A tensor representation of the board.

        Shape:
            - Output: (8, 8, C) where C is the total number of channels.

        Example:
            >>> board = chess.Board()
            >>> encoder = GridEncoder()
            >>> tensor = encoder.encode(board)
            >>> tensor.shape
            torch.Size([8, 8, 30])
        """
        tensor = torch.zeros(8, 8, self.total_channels)

        self._encode_piece_placement(board, tensor)
        self._encode_controlled_squares(board, tensor)
        self._encode_castling_rights(board, tensor)
        self._encode_pins(board, tensor)

        return tensor

    def _encode_piece_placement(self, board: chess.Board, tensor: torch.Tensor) -> None:
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                rank, file = divmod(square, 8)
                channel = (piece.piece_type - 1) + (6 if piece.color == chess.BLACK else 0)
                tensor[7 - rank, file, channel] = 1

    def _encode_controlled_squares(self, board: chess.Board, tensor: torch.Tensor) -> None:
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in range(1, 7):
                for square in board.pieces(piece_type, color):
                    attacks = board.attacks(square)
                    channel = self.piece_channels + (piece_type - 1) + (6 if color == chess.BLACK else 0)
                    for attack_square in attacks:
                        rank, file = divmod(attack_square, 8)
                        tensor[7 - rank, file, channel] = 1

    def _encode_castling_rights(self, board: chess.Board, tensor: torch.Tensor) -> None:
        castling_rights = board.clean_castling_rights()
        channel = self.piece_channels + self.control_channels

        if castling_rights & chess.BB_H1:
            tensor[7, 5:7, channel] = 1
        if castling_rights & chess.BB_A1:
            tensor[7, 1:4, channel + 1] = 1
        if castling_rights & chess.BB_H8:
            tensor[0, 5:7, channel + 2] = 1
        if castling_rights & chess.BB_A8:
            tensor[0, 1:4, channel + 3] = 1

    def _encode_pins(self, board: chess.Board, tensor: torch.Tensor) -> None:
        channel = self.piece_channels + self.control_channels + self.castling_channels

        for color in [chess.WHITE, chess.BLACK]:
            for square in chess.SQUARES:
                if board.is_pinned(color, square):
                    rank, file = divmod(square, 8)
                    tensor[7 - rank, file, channel + (1 if color == chess.BLACK else 0)] = 1

    def __repr__(self) -> str:
        return (f"GridEncoder(piece_channels={self.piece_channels}, "
                f"control_channels={self.control_channels}, "
                f"castling_channels={self.castling_channels}, "
                f"pin_channels={self.pin_channels})")