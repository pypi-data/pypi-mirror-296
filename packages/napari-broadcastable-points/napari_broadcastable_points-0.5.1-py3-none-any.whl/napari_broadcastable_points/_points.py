from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple, Union

import numpy as np
from napari.layers import Points

from ._slice import _PointSliceRequest, _ThickNDSlice

if TYPE_CHECKING:
    from napari.layers.utils._slice_input import _SliceInput

__all__ = [
    "BroadcastablePoints",
]


class BroadcastablePoints(Points):
    def __init__(
        self, data=None, *, ndim=None, broadcast_dims: List[int] = None, **kwargs
    ):
        """
        Parameters
        ----------
        data :
        """
        if broadcast_dims is None:
            broadcast_dims = []
        # sort to ensure the for loop works correctly
        self._broadcast_dims = sorted(broadcast_dims)
        if data is not None:
            for b in broadcast_dims:
                # need to loop so because doing all at once means that larger
                # values for dim will be placed in the wrong spot
                # data = np.insert(data, b, -np.ones(data.shape[0]), axis=1)
                data = np.insert(data, b, 0, axis=1)

        super().__init__(data, ndim=ndim, **kwargs)

    def last_displayed(self) -> np.ndarray:
        """
        Return the XY coordinates of the most recently displayed points

        Returns
        -------
        data : (N, 2)
            The xy coordinates of the most recently displayed points.
        """
        return self._view_data

    # for napari > 0.4.18
    def _make_slice_request_internal(self, slice_input: _SliceInput, dims_indices):
        from napari_broadcastable_points._slice import _PointSliceRequest

        self._lastResponse = _PointSliceRequest(
            dims=slice_input,
            broadcast_dims=self._broadcast_dims,
            data=self.data,
            dims_indices=dims_indices,
            out_of_slice_display=self.out_of_slice_display,
            size=self.size,
        )
        return self._lastResponse

    def _make_slice_request_internal(
        self, slice_input: _SliceInput, data_slice: _ThickNDSlice
    ) -> _PointSliceRequest:
        self._lastResponse = _PointSliceRequest(
            slice_input=slice_input,
            data=self.data,
            data_slice=data_slice,
            projection_mode=self.projection_mode,
            out_of_slice_display=self.out_of_slice_display,
            size=self.size,
        )
        return self._lastResponse

    def _slice_data(self, dims_indices) -> Tuple[List[int], Union[float, np.ndarray]]:
        """Determines the slice of points given the indices.

        Parameters
        ----------
        dims_indices : sequence of int or slice
            Indices to slice with.

        Returns
        -------
        slice_indices : list
            Indices of points in the currently viewed slice.
        scale : float, (N, ) array
            If in `out_of_slice_display` mode then the scale factor of points, where
            values of 1 corresponds to points located in the slice, and values
            less than 1 correspond to points located in neighboring slices.
        """
        # Get a list of the data for the points in this slice
        not_disp = list(self._slice_input.not_displayed)

        ############################################################
        # start patch
        # ignore any dims we are broadcasting over
        for dim in self._broadcast_dims:
            if dim in not_disp:
                # if check to avoid errors when empty
                not_disp.remove(dim)
        # end patch
        ############################################################

        # We want a numpy array so we can use fancy indexing with the non-displayed
        # indices, but as dims_indices can (and often/always does) contain slice
        # objects, the array has dtype=object which is then very slow for the
        # arithmetic below. As Points._round_index is always False, we can safely
        # convert to float to get a major performance improvement.
        not_disp_indices = np.array(dims_indices)[not_disp].astype(float)

        if len(self.data) > 0:
            if self.out_of_slice_display is True and self.ndim > 2:
                distances = abs(self.data[:, not_disp] - not_disp_indices)
                view_dim = distances.shape[1]
                sizes = np.repeat(self.size, view_dim).reshape(distances.shape) / 2
                matches = np.all(distances <= sizes, axis=1)
                size_match = sizes[matches]
                size_match[size_match == 0] = 1
                scale_per_dim = (size_match - distances[matches]) / size_match
                scale_per_dim[size_match == 0] = 1
                scale = np.prod(scale_per_dim, axis=1)
                slice_indices = np.where(matches)[0].astype(int)
                return slice_indices, scale

            data = self.data[:, not_disp]
            distances = np.abs(data - not_disp_indices)
            matches = np.all(distances <= 0.5, axis=1)
            slice_indices = np.where(matches)[0].astype(int)
            return slice_indices, 1

        return [], np.empty(0)
